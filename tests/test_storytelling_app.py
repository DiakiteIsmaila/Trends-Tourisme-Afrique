"""Integration checks using Streamlit's actual rerun and widget machinery."""

import re
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import streamlit as st
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "dashboard/app.py"
COUNTRIES = ["Afrique du Sud", "Égypte", "Kenya", "Maroc", "Maurice", "Tanzanie", "Tunisie"]


def section(app, label, index=0):
    return [item for item in app.expander if item.label == label][index]


def text(block):
    return "\n".join(str(item.value) for kind in ("markdown", "caption", "info") for item in block.get(kind))


TRENDS = "📖 Comprendre les tendances touristiques"
ORIGIN = "🌍 Comprendre les marchés d'origine"
MAP = "🗺️ Comprendre les dynamiques territoriales"


class StorytellingAppTests(unittest.TestCase):
    def test_map_renders_shared_module_text(self):
        import src.storytelling as storytelling
        with patch("src.storytelling.national_observations", wraps=storytelling.national_observations) as shared:
            app = self.start()
            self.assertIn("En 2019, la Tanzanie a enregistré 1 527 000 arrivées touristiques internationales.",
                          text(section(app, MAP)))
            self.assertTrue(any(call.args[2:] == ("arrivals", (2019, 2019)) for call in shared.call_args_list))
            original_chart = st.plotly_chart

            def selected_chart(*args, **kwargs):
                original_chart(*args, **kwargs)
                return SimpleNamespace(selection=SimpleNamespace(points=[{
                    "customdata": ["Tanzanie", 2019, "source", "persons"], "location": "TZA",
                }]))

            with patch("streamlit.plotly_chart", side_effect=selected_chart):
                shared.reset_mock()
                app.run()
                self.assertFalse(app.exception)
                self.assertIn("En 2019, la Tanzanie a enregistré 1 527 000 arrivées touristiques internationales.",
                              text(section(app, MAP)))
                self.assertTrue(any(call.args[1:] == (["Tanzanie"], "arrivals", (2019, 2019))
                                    for call in shared.call_args_list))

    def start(self):
        app = AppTest.from_file(str(APP), default_timeout=30).run()
        self.assertFalse(app.exception)
        return app

    def test_all_destinations_and_original_exports(self):
        app = self.start()
        for country in COUNTRIES:
            with self.subTest(country=country):
                app.multiselect(key="trend_destinations").set_value([country])
                app.selectbox(key="origin_destination").set_value(country).run()
                self.assertFalse(app.exception)
                self.assertIn(country, text(section(app, TRENDS)))
                self.assertIn("Contexte documentaire", text(section(app, ORIGIN)))
                self.assertGreaterEqual(len(app.get("download_button")), 6)
                self.assertEqual(len(app.get("plotly_chart")), 1)
                if country == "Kenya":
                    self.assertIn("adoption non confirmée", text(section(app, ORIGIN)))
                if country == "Tunisie":
                    self.assertIn("Référence bibliographique à confirmer", text(section(app, ORIGIN)))

    def test_periods_indicators_and_fixed_comparisons(self):
        app = self.start()
        app.multiselect(key="trend_destinations").set_value(["Maroc"])
        for period in [(2005, 2010), (2020, 2020)]:
            app.slider(key="trend_year_range").set_value(period).run()
            self.assertFalse(app.exception)
            self.assertIn(f"{period[0]}–{period[1]}", text(section(app, TRENDS)))
            self.assertIn("2019", text(section(app, TRENDS, 3)))
            self.assertIn("indépendante du filtre", text(section(app, TRENDS, 3)))
        app.selectbox(key="trend_indicator").set_value("Recettes touristiques").run()
        self.assertFalse(app.exception)
        self.assertIn("USD courants", text(section(app, TRENDS)))
        self.assertIn("ni dépense individuelle", text(section(app, TRENDS, 2)))
        for dimension in ("Variation annuelle médiane pré-2020", "Volatilité pré-2020"):
            app.radio(key="trend_comparison").set_value(dimension).run()
            self.assertFalse(app.exception)
            self.assertIn("22 variations annuelles communes", text(section(app, TRENDS, 3)))
            self.assertIn("1998–2019", text(section(app, TRENDS, 3)))

    def test_missing_empty_and_egypt_actual_panels(self):
        app = self.start()
        app.multiselect(key="trend_destinations").set_value(["Kenya"])
        app.slider(key="trend_year_range").set_value((2020, 2020)).run()
        self.assertFalse(app.exception)
        self.assertIn("aucune valeur disponible", text(section(app, TRENDS)))
        app.multiselect(key="trend_destinations").set_value([]).run()
        self.assertFalse(app.exception)
        for index in range(4):
            self.assertIn("Aucune destination sélectionnée", text(section(app, TRENDS, index)))
        app.selectbox(key="origin_destination").set_value("Tunisie").run()
        app.selectbox(key="origin_year").set_value(2017).run()
        self.assertFalse(app.exception)
        self.assertIn("les données sont manquantes", text(section(app, ORIGIN)))
        app.selectbox(key="origin_destination").set_value("Égypte").run()
        app.selectbox(key="origin_year").set_value(2010).run()
        narrative = text(section(app, ORIGIN))
        self.assertIn("En 2010", narrative)
        self.assertIn("En 2019", narrative)
        app.selectbox(key="origin_category").set_value("country").run()
        self.assertNotIn("En 2019", text(section(app, ORIGIN)))
        app.selectbox(key="origin_category").set_value("regional_aggregate").run()
        self.assertNotIn("En 2010", text(section(app, ORIGIN)))
        self.assertIn("En 2019", text(section(app, ORIGIN)))
        self.assertFalse(app.exception)

    def test_map_no_arbitrary_country_and_selected_country(self):
        app = self.start()
        self.assertNotIn("Contexte documentaire", text(section(app, MAP)))
        app.selectbox(key="map_year").set_value(2020).run()
        self.assertFalse(app.exception)
        self.assertIn("4/7 destinations couvertes", text(section(app, MAP)))
        self.assertIn("internationales au Kenya", text(section(app, MAP)))
        original_chart = st.plotly_chart

        def selected_chart(*args, **kwargs):
            original_chart(*args, **kwargs)
            return SimpleNamespace(selection=SimpleNamespace(points=[{
                "customdata": ["Maroc", 2020, "source", "persons"], "location": "MAR",
            }]))

        with patch("streamlit.plotly_chart", side_effect=selected_chart):
            app.run()
            self.assertFalse(app.exception)
            self.assertIn("CESE", text(section(app, MAP)))
            self.assertNotIn("OCDE", text(section(app, MAP)))
            app.selectbox(key="map_indicator").set_value("Recettes touristiques").run()
            self.assertFalse(app.exception)
            self.assertNotIn("Contexte documentaire", text(section(app, MAP)))
            self.assertIn("USD courants", text(section(app, MAP)))

    def test_existing_charts_tables_filters_and_exports_unchanged(self):
        # Remove only the additive storytelling blocks to run the existing UI.
        source = APP.read_text(encoding="utf-8")
        baseline = re.sub(r"^[ \t]*# STORYTELLING START[^\n]*\n.*?^[ \t]*# STORYTELLING END\n",
                          "", source, flags=re.MULTILINE | re.DOTALL)
        baseline = baseline.replace("Path(__file__).resolve().parents[1]", f"Path({str(ROOT)!r})")
        before = AppTest.from_string(baseline, default_timeout=30).run()
        after = self.start()
        self.assertFalse(before.exception)
        for app in (before, after):
            app.multiselect(key="trend_destinations").set_value(["Maroc", "Kenya"])
            app.slider(key="trend_year_range").set_value((2005, 2010))
            app.selectbox(key="origin_destination").set_value("Tanzanie").run()
            self.assertFalse(app.exception)
        for kind in ("arrow_vega_lite_chart", "plotly_chart"):
            old, new = before.get(kind), after.get(kind)
            self.assertEqual(len(old), len(new))
            for left, right in zip(old, new):
                self.assertEqual(left.proto.spec, right.proto.spec)
        self.assertEqual(len(before.dataframe), len(after.dataframe))
        for left, right in zip(before.dataframe, after.dataframe):
            self.assertTrue(left.value.equals(right.value))
        for kind in ("selectbox", "multiselect", "slider", "radio"):
            self.assertEqual([(x.key, x.value) for x in before.get(kind)],
                             [(x.key, x.value) for x in after.get(kind)])
        old, new = before.get("download_button"), after.get("download_button")
        self.assertEqual(len(old), len(new))
        for left, right in zip(old, new):
            self.assertEqual(left.proto.label, right.proto.label)
            self.assertEqual(left.proto.url, right.proto.url)


if __name__ == "__main__":
    unittest.main()
