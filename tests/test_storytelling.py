"""Tests unitaires : les petits jeux synthétiques sont des fixtures de test uniquement."""

from pathlib import Path
import unittest

import pandas as pd

from src.storytelling import (
    COUNTRY_ANALYSES, build_story, comparison_observations,
    get_country_analysis, national_observations, provenance_observations,
)


def national_fixture(values, receipts=None):
    rows = []
    for layer, observations, unit in (
        ("arrivals", values, "persons"),
        ("receipts", receipts or {}, "current_USD"),
    ):
        for year, value in observations.items():
            rows.append(dict(destination="Maroc", year=year, value=value, unit=unit,
                             granularity="destination_total", dataset_layer=layer))
    return pd.DataFrame(rows)


class StorytellingTests(unittest.TestCase):
    def test_single_year_all_countries_and_all_national_years(self):
        path = Path(__file__).resolve().parents[1] / "data/final/dataset_maitre_trends_tourisme_afrique.csv"
        data = pd.read_csv(path)
        for indicator in ("arrivals", "receipts"):
            national = data.loc[data.dataset_layer.eq(indicator)]
            for year in sorted(national.year.unique()):
                observations = national_observations(data, COUNTRY_ANALYSES, indicator, (int(year), int(year)))
                for observation in observations:
                    with self.subTest(indicator=indicator, year=year, country=observation.destination):
                        row = national.loc[national.destination.eq(observation.destination) & national.year.eq(year)].iloc[0]
                        self.assertNotIn(f"{year}–{year}", observation.text)
                        self.assertNotIn("année(s)", observation.text)
                        if pd.isna(row.value):
                            self.assertEqual(observation.missing_count, 1)
                            self.assertIn("aucune valeur disponible", observation.text)
                            self.assertNotIn("a enregistré 0", observation.text)
                        else:
                            self.assertEqual(observation.missing_count, 0)
                            self.assertIn("Les données sont disponibles pour cette destination et cette année.", observation.text)
                            if indicator == "arrivals":
                                amount = f"{row.value:,.0f}".replace(",", " ")
                                self.assertIn(f"a enregistré {amount} arrivées touristiques internationales.", observation.text)
                            else:
                                self.assertIn("USD courants", observation.text)
        tanzania, = national_observations(data, ["Tanzanie"], "arrivals", (2019, 2019))
        self.assertEqual(tanzania.text, "En 2019, la Tanzanie a enregistré 1 527 000 arrivées touristiques internationales. Les données sont disponibles pour cette destination et cette année.")

    def test_kenya_2023_french_partial_panel_regression(self):
        path = Path(__file__).resolve().parents[1] / "data/final/dataset_maitre_trends_tourisme_afrique.csv"
        data = pd.read_csv(path)
        selected = data.loc[data.dataset_layer.eq("provenance") & data.destination.eq("Kenya")
                            & data.year.eq(2023) & data.granularity.eq("country")]
        before = selected.copy(deep=True)
        observation, = provenance_observations(selected)
        self.assertIn("États-Unis", observation.text)
        self.assertIn("265 310 arrivées", observation.text)
        self.assertIn("couverture est partielle", observation.text)
        self.assertIn("Top 30", observation.text)
        for old in ("265 310,00", "observation(s)", "valeur(s)", "United States", "à égalité"):
            self.assertNotIn(old, observation.text)
        pd.testing.assert_frame_equal(before, selected)

    def test_translations_preserve_territories_and_unknown_labels(self):
        data = self.provenance_fixture().assign(destination="Maurice", unit="persons",
                                               quality_flag="exact_main7")
        data["origin_name"] = ["Reunion Island", "France", "Unknown market"]
        data["value"] = [300., 200., None]
        observation, = provenance_observations(data)
        self.assertIn("La Réunion (territoire)", observation.text)
        self.assertIn("Unknown market", observation.text)
        self.assertIn("panel de 7 marchés", observation.text)
        self.assertEqual(observation.available_count, 2)
        self.assertIn("marché distinct de France", " ".join(observation.limits))

    def test_granularity_is_preserved_in_translations(self):
        base = self.provenance_fixture().iloc[:1].copy()
        for name, granularity, expected in [
            ("Europeans", "regional_aggregate", "Européens"),
            ("MRE", "diaspora", "diasporas"),
            ("United Nations Organization", "institutional_category", "catégories institutionnelles"),
        ]:
            with self.subTest(granularity=granularity):
                data = base.assign(origin_name=name, granularity=granularity, value=float("nan"))
                observation, = provenance_observations(data)
                self.assertIn(expected, observation.text)
                if granularity == "institutional_category":
                    self.assertIn("Organisation des Nations unies (ONU)", observation.text)

    def test_all_partial_panel_labels_and_ties(self):
        for flag, expected in [("exact_top30", "Top 30"), ("exact_panel18", "18 marchés"),
                               ("exact_main7", "7 marchés"), ("survey_share_top15", "Top 15"),
                               ("exact_single_country", "un seul marché pays"),
                               ("regional_share_only", "parts régionales")]:
            with self.subTest(flag=flag):
                observation, = provenance_observations(self.provenance_fixture().assign(quality_flag=flag))
                self.assertIn("couverture est partielle", observation.text)
                self.assertIn(expected, observation.text)
                self.assertIn("à égalité", observation.text)

    def test_natural_arrivals_and_complete_period(self):
        data = national_fixture({2005: 6080000., 2006: 7000000., 2007: 9780000.})
        observation, = national_observations(data, ["Maroc"], "arrivals", (2005, 2007))
        self.assertIn("Entre 2005 et 2007", observation.text)
        self.assertIn("de 6 080 000 à 9 780 000", observation.text)
        self.assertIn("progression de 60,9 %", observation.text)
        self.assertIn("Les données sont disponibles pour toutes les années sélectionnées.", observation.text)
        for technical in ("première valeur disponible", "année(s)", "non annualisée", "6 080 000,00"):
            self.assertNotIn(technical, observation.text)

    def test_receipts_scale_and_actual_bounds(self):
        data = national_fixture({2017: 10., 2018: 20.}, {2017: 2500000., 2018: 1250000000.})
        observation, = national_observations(data, ["Maroc"], "receipts", (2016, 2019))
        self.assertIn("Entre 2017 et 2018", observation.text)
        self.assertIn("2,50 millions USD courants", observation.text)
        self.assertIn("1,25 milliards USD courants", observation.text)
        self.assertIn("années suivantes : 2016, 2019", observation.text)
        self.assertEqual(observation.missing_count, 2)

    def test_missing_years_and_uncalculable_changes_are_distinct(self):
        data = national_fixture({2017: 0., 2018: 100., 2020: 50.})
        level, = national_observations(data, ["Maroc"], "arrivals", (2017, 2020))
        self.assertIn("années suivantes : 2019", level.text)
        annual, = national_observations(data, ["Maroc"], "arrivals", (2018, 2020), annual=True)
        self.assertIn("ne peut pas être calculée", annual.text)
        self.assertIn("2018, 2019, 2020", annual.text)
        self.assertNotIn("Les données ne sont pas disponibles", annual.text)

    def test_decline_stability_and_small_percentage(self):
        for last, expected in [(90., "baisse de 10 %"), (100., "une stabilité"),
                               (100.01, "progression de moins de 0,1 %")]:
            with self.subTest(last=last):
                data = national_fixture({2017: 100., 2018: last})
                observation, = national_observations(data, ["Maroc"], "arrivals", (2017, 2018))
                self.assertIn(expected, observation.text)

    def test_provenance_integer_counts_and_named_missing_origins(self):
        data = self.provenance_fixture().assign(unit="persons", metric_type="tourist_arrivals")
        data["value"] = [123456., 100000., None]
        observation, = provenance_observations(data)
        self.assertIn("123 456 arrivées", observation.text)
        self.assertNotIn("123 456,00", observation.text)
        self.assertIn("données sont manquantes pour : C", observation.text)
        data = self.provenance_fixture()
        data["value"] = [.12345, .1, None]
        observation, = provenance_observations(data)
        self.assertIn("12,3 %", observation.text)
        self.assertNotIn("12,35", observation.text)

    def test_seven_documentary_profiles_are_complete(self):
        self.assertEqual(set(COUNTRY_ANALYSES), {
            "Afrique du Sud", "Égypte", "Kenya", "Maroc", "Maurice", "Tanzanie", "Tunisie",
        })
        for country, document in COUNTRY_ANALYSES.items():
            with self.subTest(country=country):
                self.assertEqual(document.destination, country)
                self.assertTrue(document.context and document.context.strip())
                self.assertTrue(document.action_paths)
                self.assertTrue(all(action.strip() for action in document.action_paths))
                self.assertTrue(document.limits)
                self.assertTrue(all(limit.strip() for limit in document.limits))
                self.assertTrue(document.references)
                self.assertTrue(all(ref.citation.strip() for ref in document.references))
                self.assertNotIn("en attente", " ".join(document.limits))

    def test_documentary_sources_do_not_invent_missing_details(self):
        for document in COUNTRY_ANALYSES.values():
            self.assertIsNone(document.references[0].validated_text)
            self.assertIsNone(document.references[0].url)
            self.assertIsNone(document.references[0].pages)
        self.assertIn("adoption non confirmée", get_country_analysis("Kenya").references[0].status)
        self.assertIsNone(get_country_analysis("Égypte").references[0].year)

    def test_documentary_reservations_are_preserved(self):
        kenya = get_country_analysis("Kenya")
        self.assertIn("projet de stratégie (draft)", kenya.limits[0])
        self.assertIn("projet de juin 2025", kenya.references[0].citation)
        tunisia = get_country_analysis("Tunisie")
        self.assertIn("Référence bibliographique à confirmer", tunisia.references[0].citation)
        self.assertIn("Référence bibliographique à confirmer", tunisia.references[0].status)
        self.assertIn("ne peuvent pas expliquer directement les résultats de 2019", get_country_analysis("Afrique du Sud").limits[0])
        self.assertIn("postérieure aux données de 2019", get_country_analysis("Égypte").limits[0])
        self.assertIn("analyse historique", get_country_analysis("Maurice").limits[0])
        self.assertIn("référence historique", get_country_analysis("Tanzanie").limits[0])

    def test_consecutive_years_and_boundary(self):
        data = national_fixture({2017: 100., 2018: 120., 2020: 60.})
        observation, = national_observations(data, ["Maroc"], "arrivals", (2018, 2020), annual=True)
        self.assertEqual(observation.available_count, 1)
        self.assertEqual(observation.missing_count, 2)
        self.assertIn("20 %", observation.text)
        self.assertIn("par rapport à 2017", observation.text)

    def test_missing_and_zero_base(self):
        data = national_fixture({2017: 0., 2018: 100., 2019: None, 2020: 50.})
        observation, = national_observations(data, ["Maroc"], "arrivals", (2017, 2020), annual=True)
        self.assertEqual(observation.available_count, 0)
        self.assertEqual(observation.missing_count, 4)
        level, = national_observations(data, ["Maroc"], "arrivals", (2017, 2017))
        self.assertEqual(level.available_count, 1)
        self.assertIn("a enregistré 0 arrivées", level.text)

    def test_ratio_pairs_and_non_mutation(self):
        data = national_fixture({2017: 10., 2018: 0., 2019: None},
                                {2017: 200., 2018: 100., 2020: 150.})
        before = data.copy(deep=True)
        observation, = national_observations(data, ["Maroc"], "ratio", (2017, 2020))
        self.assertEqual(observation.available_count, 1)
        self.assertEqual(observation.missing_count, 3)
        self.assertIn("20,00 USD courants par arrivée", observation.text)
        self.assertIn("ni dépense individuelle", " ".join(observation.limits))
        pd.testing.assert_frame_equal(before, data)
        with self.assertRaises(ValueError):
            national_observations(data, ["Maroc"], "ratio", (2017, 2020), annual=True)

    def test_empty_selection_and_no_observation(self):
        data = national_fixture({2019: 100.})
        self.assertEqual(national_observations(data, [], "arrivals", (2019, 2019)), ())
        observation, = national_observations(data, ["Maroc"], "arrivals", (2022, 2024))
        self.assertEqual(observation.missing_count, 3)
        self.assertIn("aucune valeur", observation.text)
        self.assertEqual(provenance_observations(self.provenance_fixture().iloc[:0]), ())

    def test_invalid_input(self):
        data = national_fixture({2019: 100.})
        with self.assertRaises(ValueError):
            national_observations(pd.concat([data, data]), ["Maroc"], "arrivals", (2019, 2019))
        with self.assertRaises(ValueError):
            national_observations(data, ["Maroc"], "arrivals", (2020, 2019))
        with self.assertRaises(ValueError):
            national_observations(data.assign(unit="share"), ["Maroc"], "arrivals", (2019, 2019))
        with self.assertRaises(ValueError):
            national_observations(data.assign(value=float("inf")), ["Maroc"], "arrivals", (2019, 2019))

    @staticmethod
    def provenance_fixture():
        return pd.DataFrame([
            dict(destination="Tanzanie", year=2024, origin_name=name,
                 granularity="country", metric_type="source_market_share", unit="share",
                 coverage_scope="top15", quality_flag="survey_share_top15", value=value)
            for name, value in [("A", .2), ("B", .2), ("C", None)]
        ])

    def test_partial_provenance_missing_ties_and_shares(self):
        data = self.provenance_fixture()
        before = data.copy(deep=True)
        observation, = provenance_observations(data)
        self.assertEqual(observation.missing_count, 1)
        self.assertIn("avec 20 %", observation.text)
        self.assertIn("aucune exhaustivité", " ".join(observation.limits))
        self.assertIn("renormalisation", " ".join(observation.limits))
        pd.testing.assert_frame_equal(before, data)
        with self.assertRaises(ValueError):
            provenance_observations(data.assign(value=20.))
        with self.assertRaises(ValueError):
            provenance_observations(pd.concat([data, data]))

    def test_separate_periods_and_measures(self):
        data = self.provenance_fixture().iloc[:1]
        combined = pd.concat([data, data.assign(year=2023),
                              data.assign(metric_type="regional_tourist_nights_share")])
        self.assertEqual(len(provenance_observations(combined)), 3)

    def test_story_country_consistency(self):
        data = national_fixture({2019: 100.})
        observations = national_observations(data, ["Maroc"], "arrivals", (2019, 2019))
        story = build_story("Maroc", observations)
        self.assertEqual(story.observations, observations)
        self.assertEqual(story.documentary, get_country_analysis("Maroc"))
        self.assertTrue(story.documentary.context)
        with self.assertRaises(ValueError):
            build_story("Kenya", observations)

    def test_real_master_all_countries_and_comparison(self):
        path = Path(__file__).resolve().parents[1] / "data/final/dataset_maitre_trends_tourisme_afrique.csv"
        data = pd.read_csv(path)
        before = data.copy(deep=True)
        for indicator in ("arrivals", "receipts", "ratio"):
            self.assertEqual(len(national_observations(data, COUNTRY_ANALYSES, indicator, (1995, 2020))), 7)
        for indicator in ("arrivals", "receipts"):
            for dimension in ("level", "median", "volatility"):
                observations = comparison_observations(data, COUNTRY_ANALYSES, indicator, dimension)
                self.assertEqual(len(observations), 7)
                for observation in observations:
                    self.assertEqual(observation.period, (2019, 2019) if dimension == "level" else (1998, 2019))
                    self.assertEqual(observation.available_count, 1 if dimension == "level" else 22)
        provenance = provenance_observations(data.loc[data.dataset_layer.eq("provenance")])
        self.assertEqual(sum(x.missing_count for x in provenance), 60)
        self.assertEqual({x.destination for x in provenance}, set(COUNTRY_ANALYSES))
        pd.testing.assert_frame_equal(before, data)


if __name__ == "__main__":
    unittest.main()
