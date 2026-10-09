"""Récits descriptifs indépendants de Streamlit, sans écriture ni collecte réseau.

Les contenus éditoriaux ci-dessous sont fournis et validés par le commanditaire.
Ils ne constituent pas les textes intégraux des références ; les réserves
bibliographiques et temporelles fournies sont conservées.
Les fonctions reçoivent le maître en mémoire et ne le modifient jamais.
"""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Optional

import numpy as np
import pandas as pd

from src.indicators import annual_variations, common_pre2020_summary, national_series


@dataclass(frozen=True)
class Reference:
    citation: str
    year: Optional[int] = None
    title: Optional[str] = None
    url: Optional[str] = None
    pages: Optional[str] = None
    validated_text: Optional[str] = None
    status: str = "Texte intégral absent du projet ; référence à compléter et valider."


@dataclass(frozen=True)
class DocumentaryAnalysis:
    destination: str
    references: tuple[Reference, ...]
    context: Optional[str] = None
    action_paths: tuple[str, ...] = ()
    limits: tuple[str, ...] = (
        "Contexte documentaire et pistes d'action en attente de texte validé.",
        "Une évolution statistique ne démontre pas l'effet d'une politique publique.",
    )


# Contenus éditoriaux fournis et validés par le commanditaire.
# validated_text reste réservé au texte source validé, non fourni ici.
COUNTRY_ANALYSES = MappingProxyType({
    'Afrique du Sud': DocumentaryAnalysis(
        destination='Afrique du Sud',
        references=(Reference(
            citation='OCDE, 2026, OECD Tourism Trends and Policies.',
            year=2026,
            title='OECD Tourism Trends and Policies',
            status='Contenu éditorial validé par le commanditaire ; texte intégral de la source non fourni.',
        ),),
        context="L'OCDE (2026) présente plusieurs orientations visant à améliorer l'accessibilité, la sécurité, la compétitivité et la résilience du secteur touristique sud-africain.",
        action_paths=("Renforcer les connexions aériennes, améliorer les conditions d'accueil et soutenir un développement touristique plus inclusif.",),
        limits=(
            "Les orientations récentes ne peuvent pas expliquer directement les résultats de 2019. Les chiffres de l'OCDE et ceux du dataset ne doivent pas être comparés directement sans harmonisation.",
            "Une évolution statistique ne démontre pas l'effet d'une politique publique.",
        ),
    ),
    'Égypte': DocumentaryAnalysis(
        destination='Égypte',
        references=(Reference(
            citation="Service d'information de l'État égyptien, stratégie nationale pour le tourisme durable 2030.",
            year=None,
            title=None,
            status='Contenu éditorial validé par le commanditaire ; texte intégral de la source non fourni.',
        ),),
        context='La stratégie nationale égyptienne pour le tourisme durable 2030 présente une ambition de développement touristique associée à des enjeux de durabilité.',
        action_paths=('Renforcer la valorisation du patrimoine, améliorer la qualité des infrastructures et intégrer davantage les objectifs environnementaux.',),
        limits=(
            'Cette stratégie est postérieure aux données de 2019 et ne peut pas expliquer directement les performances observées.',
            "Une évolution statistique ne démontre pas l'effet d'une politique publique.",
        ),
    ),
    'Kenya': DocumentaryAnalysis(
        destination='Kenya',
        references=(Reference(
            citation='Kenya National Tourism Strategy 2025–2030, projet de juin 2025.',
            year=2025,
            title='Kenya National Tourism Strategy 2025–2030',
            status='Contenu éditorial validé par le commanditaire ; texte intégral de la source non fourni. Projet de juin 2025 ; adoption non confirmée.',
        ),),
        context="Le projet de stratégie nationale du tourisme 2025–2030 propose de diversifier l'offre au-delà des safaris et du tourisme balnéaire, tout en renforçant la durabilité et l'inclusion.",
        action_paths=('Développer le tourisme culturel, soutenir les entreprises locales et améliorer la résilience environnementale des destinations.',),
        limits=(
            "Le document étudié est un projet de stratégie (draft) et ne constitue pas une preuve d'adoption ou de mise en œuvre.",
            "Une évolution statistique ne démontre pas l'effet d'une politique publique.",
        ),
    ),
    'Maroc': DocumentaryAnalysis(
        destination='Maroc',
        references=(Reference(
            citation="CESE, 2020, rapport sur le tourisme comme levier de développement durable et d'intégration.",
            year=2020,
            title=None,
            status='Contenu éditorial validé par le commanditaire ; texte intégral de la source non fourni.',
        ),),
        context='Le CESE (2020) souligne les enjeux de gouvernance, de concentration géographique des activités et de développement durable du tourisme marocain.',
        action_paths=('Favoriser une meilleure répartition territoriale des activités touristiques, soutenir les acteurs locaux et renforcer la durabilité des destinations.',),
        limits=(
            'Les données nationales ne permettent pas de mesurer directement les disparités entre les régions.',
            "Une évolution statistique ne démontre pas l'effet d'une politique publique.",
        ),
    ),
    'Maurice': DocumentaryAnalysis(
        destination='Maurice',
        references=(Reference(
            citation="Grégoire, 2008, Développement touristique et reproduction sociale à l'île Maurice, Civilisations.",
            year=2008,
            title="Développement touristique et reproduction sociale à l'île Maurice",
            status='Contenu éditorial validé par le commanditaire ; texte intégral de la source non fourni.',
        ),),
        context="Grégoire (2008) analyse le développement historique d'un tourisme principalement haut de gamme et soulève des questions relatives à la répartition des bénéfices économiques et à l'occupation du littoral.",
        action_paths=('Encourager les retombées locales du tourisme, diversifier les activités et préserver les espaces côtiers.',),
        limits=(
            'Cette analyse historique ne permet pas de décrire à elle seule les conditions sociales et environnementales actuelles.',
            "Une évolution statistique ne démontre pas l'effet d'une politique publique.",
        ),
    ),
    'Tanzanie': DocumentaryAnalysis(
        destination='Tanzanie',
        references=(Reference(
            citation='Ministry of Natural Resources and Tourism, 1999, National Tourism Policy.',
            year=1999,
            title='National Tourism Policy',
            status='Contenu éditorial validé par le commanditaire ; texte intégral de la source non fourni.',
        ),),
        context="La politique nationale du tourisme de 1999 identifie la diversification de l'offre, les infrastructures, la participation communautaire et la protection de l'environnement comme des priorités.",
        action_paths=('Valoriser le patrimoine culturel, renforcer la participation des communautés locales et préserver les ressources naturelles.',),
        limits=(
            "Ce document constitue une référence historique et ne permet pas d'évaluer les politiques actuellement mises en œuvre.",
            "Une évolution statistique ne démontre pas l'effet d'une politique publique.",
        ),
    ),
    'Tunisie': DocumentaryAnalysis(
        destination='Tunisie',
        references=(Reference(
            citation="Hellal, 2020, L'évolution du système touristique en Tunisie. Perspectives de gouvernance en contexte de crise, Études caribéennes. Référence bibliographique à confirmer.",
            year=2020,
            title="L'évolution du système touristique en Tunisie. Perspectives de gouvernance en contexte de crise",
            status='Contenu éditorial validé par le commanditaire ; texte intégral de la source non fourni. Référence bibliographique à confirmer.',
        ),),
        context="Hellal (2020) analyse l'évolution historique du tourisme tunisien, notamment la place du modèle balnéaire et les transformations de sa gouvernance.",
        action_paths=("Diversifier l'offre touristique, renforcer la coordination entre acteurs publics et privés et améliorer la résilience des destinations.",),
        limits=(
            "Les données nationales ne permettent pas d'évaluer directement les effets des choix de gouvernance sur les performances touristiques.",
            "Une évolution statistique ne démontre pas l'effet d'une politique publique.",
        ),
    ),
})


@dataclass(frozen=True)
class StatisticalObservation:
    destination: str
    indicator: str
    period: tuple[int, int]
    unit: str
    text: str
    available_count: int
    missing_count: int
    limits: tuple[str, ...] = ()


@dataclass(frozen=True)
class Story:
    """Sépare explicitement statistiques, contexte, actions et limites."""

    observations: tuple[StatisticalObservation, ...]
    documentary: DocumentaryAnalysis


def get_country_analysis(destination: str) -> DocumentaryAnalysis:
    """Renvoie une fiche immuable ; pays inconnu : KeyError explicite."""
    return COUNTRY_ANALYSES[destination]


def build_story(destination, observations, documentary=None) -> Story:
    """Assemble sans inférence ; accepte une fiche documentaire validée ultérieurement."""
    document = documentary if documentary is not None else get_country_analysis(destination)
    observations = tuple(observations)
    if document.destination != destination or any(
        item.destination != destination for item in observations
    ):
        raise ValueError("Toutes les composantes doivent concerner la même destination.")
    return Story(observations, document)


def _period(period):
    start, end = period
    if any(pd.isna(x) or int(x) != x for x in (start, end)) or start > end:
        raise ValueError("Période invalide : deux années entières croissantes requises.")
    return int(start), int(end)


def _validate(data, columns):
    missing = set(columns) - set(data.columns)
    if missing:
        raise ValueError(f"Colonnes requises absentes : {sorted(missing)}")
    if data.year.isna().any() or not pd.api.types.is_numeric_dtype(data.year):
        raise ValueError("Années numériques renseignées requises.")
    if not np.isfinite(data.year).all() or data.year.mod(1).ne(0).any():
        raise ValueError("Années entières finies requises.")
    values = data.value.dropna()
    if not pd.api.types.is_numeric_dtype(data.value) or not np.isfinite(values).all():
        raise ValueError("Valeurs numériques finies ou manquantes requises.")
    if values.lt(0).any():
        raise ValueError("Valeurs touristiques négatives non prises en charge.")


def _number(value, decimals=2):
    return f"{value:,.{decimals}f}".replace(",", " ").replace(".", ",")


def _percent(value):
    """Display rounding only; retain direction for very small changes."""
    if 0 < abs(value) < 0.05:
        return "moins de 0,1"
    return _number(abs(value), 1).removesuffix(",0")


def _amount(value, indicator):
    if indicator == "arrivals":
        return _number(value, 0)
    if indicator == "ratio":
        return f"{_number(value)} USD courants par arrivée"
    if abs(value) >= 1e9:
        return f"{_number(value / 1e9)} milliards USD courants"
    if abs(value) >= 1e6:
        return f"{_number(value / 1e6)} millions USD courants"
    return f"{_number(value, 0)} USD courants"


def _location(country):
    return {"Maroc": "au Maroc", "Kenya": "au Kenya", "Maurice": "à Maurice"}.get(country, f"en {country}")


def _subject(indicator):
    return {"arrivals": "les arrivées touristiques internationales",
            "receipts": "les recettes touristiques",
            "ratio": "le ratio recettes/arrivées"}[indicator]


def _change_phrase(value):
    if value == 0:
        return "une stabilité"
    return f"une {'progression' if value > 0 else 'baisse'} de {_percent(value)} %"


def _coverage(start, end, available_years, *, annual=False):
    missing_years = sorted(set(range(start, end + 1)) - set(available_years))
    if not missing_years:
        if start == end and not annual:
            return "Les données sont disponibles pour cette destination et cette année."
        return ("Les variations annuelles sont calculables pour toutes les années sélectionnées."
                if annual else "Les données sont disponibles pour toutes les années sélectionnées.")
    years = ", ".join(map(str, missing_years))
    return (f"La variation annuelle ne peut pas être calculée pour les années suivantes : {years}."
            if annual else f"Les données ne sont pas disponibles pour les années suivantes : {years}.")


def _national(data, indicator):
    _validate(data, ["destination", "year", "value", "unit", "dataset_layer", "granularity"])
    table = national_series(data, indicator)
    if table.destination.isna().any():
        raise ValueError("Destination nationale manquante.")
    return table


def national_observations(data, destinations, indicator, period, *, annual=False):
    """Un constat par pays sur la fenêtre demandée, sans classement entre années.

    Pour annual=True, t-1 peut être hors fenêtre (comme dans le dashboard).
    missing_count inclut les années absentes et les valeurs non calculables.
    Une fenêtre d'une seule année convient aussi à la carte/niveaux 2019.
    """
    start, end = _period(period)
    if annual and indicator == "ratio":
        raise ValueError("La variation annuelle du ratio n'est pas une vue du dashboard.")
    table = _national(data, indicator)
    field = "variation_pct" if annual else "value"
    if annual:
        table = annual_variations(table)
    unit = "%" if annual else {
        "arrivals": "personnes", "receipts": "USD courants",
        "ratio": "USD courants par arrivée",
    }[indicator]
    results = []
    for country in dict.fromkeys(destinations):
        rows = table.loc[table.destination.eq(country) & table.year.between(start, end)]
        available = rows.loc[rows[field].notna()].sort_values("year")
        missing = end - start + 1 - len(available)
        limits = ["Les absences ne sont jamais remplacées par zéro ; aucune causalité n'est déduite."]
        if indicator in ("receipts", "ratio"):
            limits.append("Recettes en USD courants, sans correction de l'inflation.")
        if indicator == "ratio":
            limits.append("Ratio de recettes et d'arrivées agrégées : ni dépense individuelle, ni rentabilité.")
        if annual:
            limits.append("Deux années consécutives renseignées et une base positive sont requises ; t-1 peut précéder la fenêtre.")
        if start <= 2020 <= end:
            limits.append("2020 est une rupture exceptionnelle ; ces observations seules ne mesurent pas une reprise post-Covid.")
        subject, location = _subject(indicator), _location(country)
        if available.empty:
            text = (f"Pour {subject} {location}, aucune {'variation annuelle calculable' if annual else 'valeur disponible'} "
                    + (f"en {start}." if start == end else f"sur la période sélectionnée ({start}–{end})."))
        elif annual:
            last = available.iloc[-1]
            text = (
                f"En {int(last.year)}, {subject} {location} enregistrent {_change_phrase(last[field])} "
                f"par rapport à {int(last.year) - 1}."
            )
        else:
            first, last = available.iloc[0], available.iloc[-1]
            text = f"En {int(last.year)}, {subject} {location} {'s’établit' if indicator == 'ratio' else 's’établissent'} à {_amount(last.value, indicator)}."
            if start == end and indicator == "arrivals":
                country_subject = {
                    "Afrique du Sud": "l’Afrique du Sud", "Égypte": "l’Égypte",
                    "Kenya": "le Kenya", "Maroc": "le Maroc", "Maurice": "Maurice",
                    "Tanzanie": "la Tanzanie", "Tunisie": "la Tunisie",
                }.get(country, country)
                text = (f"En {start}, {country_subject} a enregistré {_amount(last.value, indicator)} "
                        "arrivées touristiques internationales.")
            if len(available) > 1:
                text = (f"Entre {int(first.year)} et {int(last.year)}, {subject} {location} "
                        f"{'est passé' if indicator == 'ratio' else 'sont passées'} de "
                        f"{_amount(first.value, indicator)} à {_amount(last.value, indicator)}")
                if first.value > 0:
                    change = 100 * (last.value / first.value - 1)
                    text += f", soit {_change_phrase(change)} entre ces deux années"
                text += "."
        text += " " + _coverage(start, end, available.year, annual=annual)
        results.append(StatisticalObservation(country, indicator, (start, end), unit,
                                             text, len(available), missing, tuple(limits)))
    return tuple(results)


def comparison_observations(data, destinations, indicator, dimension):
    """Reproduit les périodes de Comparaison, sans appliquer le slider temporel.

    dimension : level, median ou volatility. Les années communes sont calculées
    sur les sept pays et les deux indicateurs, comme dans l'application.
    """
    if indicator not in ("arrivals", "receipts"):
        raise ValueError("Comparaison réservée aux arrivées et recettes.")
    if dimension == "level":
        return national_observations(data, destinations, indicator, (2019, 2019))
    if dimension not in ("median", "volatility"):
        raise ValueError("Dimension de comparaison inconnue.")
    _national(data, indicator)
    summary, years = common_pre2020_summary(data, list(COUNTRY_ANALYSES))
    field = "median_pct" if dimension == "median" else "volatility_points"
    unit = "%" if dimension == "median" else "points de pourcentage"
    period = (min(years), max(years)) if years else (1998, 2019)
    results = []
    for country in dict.fromkeys(destinations):
        rows = summary.loc[summary.destination.eq(country) & summary.indicator.eq(indicator)]
        value = rows.iloc[0][field] if len(rows) == 1 else float("nan")
        count = int(rows.iloc[0].observations) if len(rows) == 1 else 0
        subject, location = _subject(indicator), _location(country)
        if pd.isna(value):
            text = f"Les données communes sont insuffisantes pour comparer {subject} {location}."
        else:
            statistic = "la variation annuelle médiane" if dimension == "median" else "la volatilité des variations annuelles"
            formatted = (("−" if value < 0 else "+" if value > 0 else "") + _percent(value)
                         if dimension == "median" and abs(value) >= 0.05 else _percent(value))
            if dimension == "median" and 0 < abs(value) < 0.05:
                formatted += " en baisse" if value < 0 else " en hausse"
            text = (f"Entre {period[0]} et {period[1]}, {statistic} pour {subject} {location} "
                    f"s’établit à {formatted} {unit}, sur {count} variations annuelles communes.")
        limits = (
            "Périmètre commun aux sept destinations et aux deux indicateurs ; indépendant du filtre de période.",
            "Années communes : " + (", ".join(map(str, years)) or "aucune"),
            "Médiane distincte du CAGR ; volatilité = écart-type échantillonnal, sans prédiction de risque.",
            "Aucune causalité ; recettes en USD courants.",
        )
        results.append(StatisticalObservation(country, dimension, period, unit, text,
                                             count, period[1] - period[0] + 1 - count, limits))
    return tuple(results)


# Traductions d'affichage uniquement : aucune normalisation des clés du dataset.
_ORIGIN_FRENCH = {
    "country": {
        "United States of America": "États-Unis", "United States": "États-Unis",
        "Etats Unis": "États-Unis", "Americans": "Américains",
        "United Kingdom": "Royaume-Uni", "Germany": "Allemagne",
        "Italy": "Italie", "Spain": "Espagne", "Belgium": "Belgique",
        "Netherlands": "Pays-Bas", "Switzerland": "Suisse", "Sweden": "Suède",
        "Norway": "Norvège", "Denmark": "Danemark", "Poland": "Pologne",
        "Australia": "Australie", "China": "Chine", "India": "Inde",
        "Republic of Korea": "République de Corée", "South Africa": "Afrique du Sud",
        "South Sudan": "Soudan du Sud", "Namibia": "Namibie",
        "Ethiopia": "Éthiopie", "Somalia": "Somalie", "Uganda": "Ouganda",
        "Tanzania": "Tanzanie", "United Republic of Tanzania": "Tanzanie",
        "Zambia": "Zambie", "United Arab Emirates": "Émirats arabes unis",
        "DRC": "République démocratique du Congo",
        "Democratic Republic of Congo": "République démocratique du Congo",
        "Reunion Island": "La Réunion (territoire)",
    },
    "regional_aggregate": {"Europeans": "Européens", "Arabs": "Arabes", "Others": "Autres"},
    "institutional_category": {"United Nations Organization": "Organisation des Nations unies (ONU)"},
    "aggregate_total": {"Touristes Etrangers": "Touristes étrangers"},
}


def _origin_label(name, granularity):
    """Conserve le libellé source lorsqu'aucune traduction explicite n'est connue."""
    return _ORIGIN_FRENCH.get(granularity, {}).get(name, name)


def provenance_observations(displayed):
    """Décrit le périmètre déjà filtré par l'appelant, sans total artificiel.

    Passer séparément les panneaux égyptiens si nécessaire : chaque groupe garde
    sa véritable année. missing_count compte les lignes manquantes publiées,
    jamais les marchés non couverts, dont le nombre n'est pas connu.
    """
    groups = ["destination", "year", "granularity", "metric_type", "unit",
              "coverage_scope", "quality_flag"]
    _validate(displayed, groups + ["value", "origin_name"])
    if displayed[groups + ["origin_name"]].isna().any().any():
        raise ValueError("Métadonnées de provenance incomplètes.")
    if not displayed.unit.isin(["persons", "share"]).all():
        raise ValueError("Unité de provenance non prise en charge.")
    if displayed.loc[displayed.unit.eq("share"), "value"].dropna().gt(1).any():
        raise ValueError("Les parts doivent être des fractions entre 0 et 1.")
    identity = [x for x in groups if x not in ("quality_flag", "coverage_scope")] + ["origin_name"]
    if displayed.duplicated(identity).any():
        raise ValueError("Observations de provenance dupliquées ou ambiguës.")
    results = []
    for key, rows in displayed.groupby(groups, sort=False, dropna=False):
        country, year, granularity, metric, unit, scope, quality = key
        available = rows.loc[rows.value.notna()]
        missing = len(rows) - len(available)
        measure = {"regional_tourist_share": "la part des touristes",
                   "regional_tourist_nights_share": "la part des nuitées",
                   "source_market_share": "la part des marchés d’origine",
                   "diaspora_arrivals": "les arrivées de la diaspora"}.get(metric, "les arrivées touristiques")
        category = {"country": "pays ou territoires", "regional_aggregate": "agrégats régionaux",
                    "diaspora": "diasporas", "institutional_category": "catégories institutionnelles",
                    "aggregate_total": "totaux agrégés"}.get(granularity, granularity)
        text = (f"En {int(year)}, les données {_location(country)} renseignent {measure} "
                f"pour {len(available)} {'origine' if len(available) == 1 else 'origines'} dans le groupe des {category}.")
        if missing:
            names_missing = ", ".join(_origin_label(name, granularity)
                                      for name in rows.loc[rows.value.isna(), "origin_name"])
            text += f" Pour cette année, les données sont manquantes pour : {names_missing}."
        else:
            text += " Toutes les observations de ce groupe publié sont renseignées."
        panel = {
            "exact_top30": "le Top 30 publié",
            "exact_panel18": "le panel de 18 marchés",
            "exact_main7": "le panel de 7 marchés",
            "survey_share_top15": "le Top 15 publié sous forme de parts",
            "exact_single_country": "un seul marché pays",
            "regional_share_only": "les parts régionales publiées",
        }.get(quality)
        if panel:
            text += (f" La couverture est partielle : {panel}. "
                     "Elle ne permet pas de décrire l'ensemble des marchés touristiques de la destination.")
        else:
            text += " Cette lecture reste limitée au périmètre publié et ne présume pas une couverture exhaustive."
        limits = [f"Couverture : {scope}. Qualité : {quality}.",
                  "Lecture limitée aux observations publiées ; aucune exhaustivité nationale présumée.",
                  "Ne pas additionner agrégats, pays, diasporas et catégories institutionnelles."]
        if not available.empty and granularity in ("country", "regional_aggregate"):
            maximum = available.value.max()
            names = ", ".join(_origin_label(name, granularity)
                              for name in available.loc[available.value.eq(maximum), "origin_name"])
            formatted = _percent(maximum * 100) if unit == "share" else _number(maximum, 0)
            tied = available.value.eq(maximum).sum() > 1
            text += (f" {'Les valeurs les plus élevées' if tied else 'La valeur la plus élevée'} "
                     f"parmi les origines renseignées de ce groupe "
                     f"{'concernent' if tied else 'concerne'} : {names}, "
                     f"avec {formatted} {'%' if unit == 'share' else 'arrivées'}"
                     f"{' pour chaque origine, à égalité' if tied else ''}.")
        if unit == "share":
            limits.append("Parts publiées : aucune conversion en volumes ni renormalisation à 100 %.")
        if country == "Égypte":
            limits.append("Aucun classement global des marchés égyptiens ; touristes et nuitées restent distincts, panneau régional 2019.")
        if country == "Maurice":
            limits.append("Réunion reste un marché distinct de France.")
        if country == "Tunisie":
            limits.append("Les absences non vérifiées ne sont pas des zéros ; Scandinaves est un agrégat de composition à vérifier.")
        if country == "Kenya":
            limits.append("L'ONU est une catégorie institutionnelle, pas un pays.")
        results.append(StatisticalObservation(country, metric, (int(year), int(year)),
                                             unit, text, len(available), missing, tuple(limits)))
    return tuple(results)
