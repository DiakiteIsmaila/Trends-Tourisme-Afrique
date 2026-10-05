from __future__ import annotations

from pathlib import Path
import re

import altair as alt
import pandas as pd
import streamlit as st

# Plotly est utilisé uniquement pour l'onglet Carte.
# L'application reste explicite si la dépendance n'est pas disponible.
try:
    import plotly.express as px
    HAS_PLOTLY = True
except Exception:
    HAS_PLOTLY = False


# ==============================================================================
# 1. CONFIGURATION GÉNÉRALE DE LA PAGE
# ==============================================================================
# Cette configuration doit être exécutée avant les autres commandes Streamlit.

st.set_page_config(
    page_title="Trends — Tourisme international en Afrique",
    layout="wide",
)

st.title("Trends — Tourisme international en Afrique")

st.caption(
    "Analyse comparative des arrivées, recettes et provenances touristiques "
    "dans sept destinations africaines."
)


# ==============================================================================
# 2. IDENTITÉ VISUELLE — PALETTE CORPORATE GAEA21
# ==============================================================================
# La palette reprend le modèle fourni par Gaea21 : fond beige, texte sombre,
# vert comme couleur d'accent et tons naturels complémentaires.

CORP = {
    "bg": "#f5f0e6",
    "panel": "#e7dfcf",
    "text": "#2e2b26",
    "accent": "#6b8e23",
    "accent2": "#8f9779",
    "brown": "#8b6b4a",
}

st.markdown(
    f"""
    <style>

        /* ==============================================================
           FOND GÉNÉRAL
           ============================================================== */

        .stApp {{
            background-color: {CORP["bg"]};
            color: {CORP["text"]};
        }}

        .block-container {{
            background: transparent;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}


        /* ==============================================================
           TEXTE GÉNÉRAL
           ============================================================== */

        /* ==============================================================
           TITRES
           ============================================================== */

        h1, h2, h3, h4, h5, h6 {{
            color: {CORP["text"]} !important;
        }}


        /* ==============================================================
           KPI / METRICS
           ============================================================== */

        [data-testid="stMetric"] {{
            color: {CORP["text"]} !important;
        }}

        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] *,
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] * {{
            color: {CORP["text"]} !important;
        }}


        /* ==============================================================
           SELECTBOX / MULTISELECT / INPUTS
           ============================================================== */

        /* ==============================================================
           SLIDER
           ============================================================== */

        [data-testid="stSlider"] {{
            color: {CORP["text"]} !important;
        }}

        [data-testid="stSlider"] span {{
            color: {CORP["text"]} !important;
        }}


        /* ==============================================================
           ONGLETS
           ============================================================== */

        .stTabs [role="tablist"] button[role="tab"] {{
            color: {CORP["text"]} !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            padding-left: 1.2rem !important;
            padding-right: 1.2rem !important;
        }}

        .stTabs [role="tablist"] button[aria-selected="true"] {{
            color: {CORP["accent"]} !important;
            border-bottom: 4px solid {CORP["accent"]} !important;
            font-weight: 700 !important;
        }}

        .stTabs [role="tablist"] button[role="tab"]:hover {{
            color: {CORP["accent"]} !important;
        }}


        /* ==============================================================
           EXPANDERS
           ============================================================== */

        [data-testid="stExpander"] {{
            background-color: transparent !important;
        }}

        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary * {{
            color: {CORP["text"]} !important;
        }}


        /* ==============================================================
           TABLEAUX
           ============================================================== */

        [data-testid="stDataFrame"] {{
            color: {CORP["text"]} !important;
        }}


        /* ==============================================================
           BOUTONS
           ============================================================== */

        .stButton button,
        .stDownloadButton button {{
            color: {CORP["text"]} !important;
            background-color: {CORP["panel"]} !important;
            border: 1px solid {CORP["accent"]} !important;
            font-weight: 600 !important;
        }}

        .stButton button:hover,
        .stDownloadButton button:hover {{
            border-color: {CORP["accent"]} !important;
            color: {CORP["accent"]} !important;
        }}


        /* ==============================================================
           CAPTIONS / TEXTES SECONDAIRES
           ============================================================== */

        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] * {{
            color: #6f6a61 !important;
        }}


        /* ==============================================================
           ALERTES
           ============================================================== */

        [data-testid="stAlert"] {{
            color: {CORP["text"]} !important;
        }}

        [data-testid="stAlert"] * {{
            color: {CORP["text"]} !important;
        }}

    </style>
    """,
    unsafe_allow_html=True,
)
# ==============================================================================
# 3. CHEMINS ET CHARGEMENT DU DATASET MAÎTRE
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "final"
    / "dataset_maitre_trends_tourisme_afrique.csv"
)


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """
    Charge le dataset maître Trends depuis le fichier CSV final.

    Le cache Streamlit évite de relire le fichier à chaque interaction
    avec un filtre du dashboard.
    """
    return pd.read_csv(path)


if not DATA_PATH.exists():
    st.error(f"Dataset introuvable : {DATA_PATH}")
    st.stop()

df = load_data(DATA_PATH)


# ==============================================================================
# 4. CONSTANTES ET FONCTIONS UTILITAIRES
# ==============================================================================

# Ordre de présentation volontaire : il évite que « Égypte » apparaisse à la fin
# à cause du tri informatique des caractères accentués.
DESTINATION_ORDER = [
    "Afrique du Sud",
    "Égypte",
    "Kenya",
    "Maroc",
    "Maurice",
    "Tanzanie",
    "Tunisie",
]

# Codes ISO-3 utilisés pour la carte Plotly.
# Ils sont plus robustes que les noms de pays pour la reconnaissance géographique.
COUNTRY_ISO_MAP = {
    "Afrique du Sud": "ZAF",
    "Égypte": "EGY",
    "Kenya": "KEN",
    "Maroc": "MAR",
    "Maurice": "MUS",
    "Tanzanie": "TZA",
    "Tunisie": "TUN",
}

LAYER_LABELS = {
    "arrivals": "Arrivées",
    "receipts": "Recettes",
    "provenance": "Provenance",
}

METRIC_TYPE_LABELS = {
    "destination_total": "Total de la destination",
    "diaspora_arrivals": "Arrivées de la diaspora",
    "regional_tourist_nights_share": "Part des nuitées",
    "regional_tourist_share": "Part des touristes",
    "source_market_share": "Part du marché d’origine",
    "tourist_arrivals": "Arrivées touristiques",
}

GRANULARITY_LABELS = {
    "aggregate_total": "Total agrégé",
    "country": "Pays / territoire",
    "destination_total": "Total de la destination",
    "diaspora": "Diaspora",
    "institutional_category": "Catégorie institutionnelle",
    "regional_aggregate": "Agrégat régional",
}

UNIT_LABELS = {
    "persons": "Personnes",
    "share": "Part (%)",
    "current_USD": "USD courants",
    "current_USD_per_arrival": "USD courants par arrivée",
}

METRIC_LABELS = {
    "tourist_arrivals": "Arrivées touristiques",
    "tourism_receipts": "Recettes touristiques",
    "receipts_per_arrival": "Ratio recettes / arrivées",
}

QUALITY_FLAG_LABELS = {
    "available": "Disponible",
    "exact_aggregate": "Agrégat exact",
    "exact_country": "Donnée pays exacte",
    "exact_diaspora": "Donnée diaspora exacte",
    "exact_main7": "Panel exact de 7 marchés",
    "exact_panel18": "Panel exact de 18 marchés",
    "exact_single_country": "Donnée exacte pour un seul pays",
    "exact_top30": "Top 30 exact",
    "missing_in_source": "Valeur absente de la source",
    "missing_unverified": "Valeur manquante non vérifiée",
    "regional_share_only": "Part régionale uniquement",
    "survey_share_top15": "Top 15 issu de l’enquête",
}

COLUMN_LABELS = {
    "destination": "Destination",
    "year": "Année",
    "origin_name": "Origine",
    "granularity": "Granularité",
    "metric_type": "Indicateur",
    "value": "Valeur brute",
    "unit": "Unité",
    "coverage_scope": "Couverture",
    "quality_flag": "Qualité",
    "source_name": "Source",
    "source_reference": "Référence",
    "notes": "Notes",
    "dataset_layer": "Type de données",
}

# Locale numérique française pour Vega-Lite / Altair :
# espace insécable comme séparateur de milliers et virgule décimale.
FRENCH_NUMBER_LOCALE = {
    "decimal": ",",
    "thousands": "\u00a0",
    "grouping": [3],
    "currency": ["", "\u00a0€"],
}

def build_annual_change_comment(points, displayed, indicator_label):
    """Resolve a unique business key against the current plotted observations."""
    if not isinstance(points, list) or len(points) != 1:
        return None
    point = points[0]
    if not isinstance(point, dict) or point.get("display_indicator") != indicator_label:
        return None
    rows = displayed.loc[
        displayed.destination.eq(point.get("destination"))
        & displayed.year.eq(point.get("year"))
        & displayed.variation_pct.notna()
    ]
    if len(rows) != 1:
        return None
    row = rows.iloc[0]
    year, change = int(row.year), float(row.variation_pct)
    direction = "en hausse" if change > 0 else "en baisse" if change < 0 else "stable"
    formatted = f"{change:+.2f}".replace(".", ",").replace("-", "−")
    text = (
        f"**{row.destination} · {year}**\n\n"
        f"Variation annuelle — {indicator_label} : **{formatted} % par rapport à {year - 1}.**\n\n"
        f"Le niveau est {direction} par rapport à l'année précédente."
    )
    if row.unit == "current_USD":
        text += "\n\nLes recettes sont exprimées en USD courants, sans correction de l'inflation."
    if year == 2020:
        text += (
            "\n\nCette observation fait partie de la rupture de 2020 visible dans les séries disponibles."
            "\n\nLe dataset actuel ne contient pas suffisamment d'observations nationales "
            "postérieures à 2020 pour mesurer une reprise post-Covid."
        )
    return text




def build_level_comment(points, displayed, indicator_label, selected_layer):
    """Décrit un point de niveau observé, sans extrapolation ni classement."""
    if not isinstance(points, list) or len(points) != 1 or not isinstance(points[0], dict):
        return None
    point = points[0]
    if point.get("display_indicator") != indicator_label:
        return None
    rows = displayed.loc[
        displayed.destination.eq(point.get("destination"))
        & displayed.year.eq(point.get("year"))
        & displayed.value.notna()
    ]
    if len(rows) != 1:
        return None
    row = rows.iloc[0]
    value = float(row.value)
    if selected_layer == "arrivals":
        formatted = f"{value:,.0f} personnes".replace(",", " ")
        label = "Arrivées touristiques"
    elif selected_layer == "receipts":
        formatted = f"{value:,.0f} USD courants".replace(",", " ")
        label = "Recettes touristiques"
    else:
        formatted = f"{value:,.2f}".replace(",", " ").replace(".", ",")
        formatted += " USD courants par arrivée"
        label = "Ratio recettes / arrivées"
    text = (
        f"**{row.destination} · {int(row.year)}**\n\n"
        f"{label} : **{formatted}.**"
    )
    if selected_layer == "receipts":
        text += "\n\nLes recettes sont exprimées en USD courants, sans correction de l'inflation."
    if selected_layer == "ratio":
        text += (
            "\n\nCe ratio est calculé à partir des recettes et des arrivées agrégées. "
            "Il ne représente ni une dépense individuelle ni une mesure de rentabilité."
        )
    if int(row.year) == 2020:
        text += (
            "\n\nCette observation fait partie de la rupture exceptionnelle de 2020. "
            "Le dataset actuel ne permet pas de mesurer une reprise post-Covid au-delà de cette rupture."
        )
    return text


def build_map_comment(points, displayed, indicator_label, unit_label):
    """Décrit une destination sélectionnée sur la carte, sans classement entre pays."""
    if not isinstance(points, list) or len(points) != 1 or not isinstance(points[0], dict):
        return None
    point = points[0]
    destination = None
    customdata = point.get("customdata")
    if isinstance(customdata, (list, tuple)) and customdata:
        destination = customdata[0]
    if not destination:
        destination = point.get("hovertext") or point.get("text")
    if not destination and point.get("location"):
        iso3 = point.get("location")
        matches = displayed.loc[displayed.iso3.eq(iso3)]
        if len(matches) == 1:
            destination = matches.iloc[0].destination
    rows = displayed.loc[displayed.destination.eq(destination) & displayed.value.notna()]
    if len(rows) != 1:
        return None
    row = rows.iloc[0]
    formatted = f"{float(row.value):,.0f}".replace(",", " ")
    text = (
        f"**{row.destination} · {int(row.year)}**\n\n"
        f"{indicator_label} : **{formatted} {unit_label}.**\n\n"
        f"Source : **{row.source_name}.**"
    )
    if row.unit == "current_USD":
        text += "\n\nLes recettes sont exprimées en USD courants, sans correction de l'inflation."
    text += "\n\nCette lecture décrit uniquement la valeur observée pour la destination sélectionnée ; aucun classement n'est déduit de la carte."
    return text


def build_comparison_comment(points, displayed, field):
    """Interpret only a unique bar present in the active comparison."""
    if not isinstance(points, list) or len(points) != 1 or not isinstance(points[0], dict):
        return None
    rows = displayed
    for key in ["destination", "display_dimension", "display_period"]:
        rows = rows.loc[rows[key].eq(points[0].get(key))]
    rows = rows.loc[rows[field].notna()]
    if len(rows) != 1:
        return None
    row = rows.iloc[0]
    value = float(row[field])
    if field == "value":
        if row.unit == "current_USD":
            divisor, unit = ((1e9, "Md USD courants") if abs(value) >= 1e9
                             else (1e6, "M USD courants") if abs(value) >= 1e6
                             else (1, "USD courants"))
            formatted = f"{value / divisor:,.3f} {unit}"
        else:
            formatted = f"{value:,.0f} personnes"
        noun = "valeur"
    elif field == "median_pct":
        formatted, noun = f"{value:+.2f} %", "médiane"
    else:
        formatted, noun = f"{value:.2f} points de pourcentage", "volatilité"
    formatted = formatted.replace(",", " ").replace(".", ",").replace("-", "−")
    text = (f"**{row.destination} · {row.display_period}**\n\n"
            f"{row.display_dimension} : **{formatted}.**")
    if field != "value" and pd.notna(row.get("observations")):
        text += f"\n\nNombre d’observations : {int(row.observations)}."
    if field == "volatility_points":
        text += "\n\nUne volatilité plus élevée traduit des variations annuelles plus dispersées sur la période."
    panel = displayed.loc[
        displayed.display_dimension.eq(row.display_dimension)
        & displayed.display_period.eq(row.display_period) & displayed[field].notna()
    ]
    if len(panel) >= 2 and not panel.destination.duplicated().any():
        for extreme, adjective in [(panel[field].max(), "élevée"), (panel[field].min(), "faible")]:
            if value == extreme and panel[field].eq(extreme).sum() == 1:
                text += (f"\n\nParmi les destinations actuellement affichées disposant d’une observation "
                         f"sur {row.display_period}, cette {noun} est la plus {adjective}.")
                break
    return text



ORIGIN_SELECTION_FIELDS = [
    "destination", "year", "origin_name", "granularity", "metric", "metric_type",
    "unit", "coverage_scope", "quality_flag",
]


def build_origin_comment(points, displayed):
    """Explain one observed provenance row, without ranking unlike scopes."""
    if not isinstance(points, list) or len(points) != 1 or not isinstance(points[0], dict):
        return None
    rows = displayed
    for key in ORIGIN_SELECTION_FIELDS:
        if key not in points[0]:
            return None
        rows = rows.loc[rows[key].eq(points[0][key])]
    rows = rows.loc[rows.value.notna()]
    if len(rows) != 1:
        return None
    row = rows.iloc[0]
    granularity = {"country": "pays", "regional_aggregate": "agrégat régional",
                   "institutional_category": "catégorie institutionnelle",
                   "diaspora": "diaspora", "aggregate_total": "total agrégé"}.get(row.granularity, row.granularity)
    label = {"regional_tourist_share": "Part des touristes",
             "regional_tourist_nights_share": "Part des nuitées"}.get(
                 row.metric_type, "Part publiée pour ce marché" if row.unit == "share"
                 else "Arrivées enregistrées pour cette origine")
    value = (f"{row.value * 100:.2f} %" if row.unit == "share" else f"{row.value:,.0f} personnes")
    value = value.replace(",", " ").replace(".", ",")
    notes = []
    panel = {"exact_top30": "Top 30 disponible", "exact_main7": "panel de 7 marchés retenus",
             "exact_panel18": "panel de 18 marchés disponible", "survey_share_top15": "Top 15 disponible"}.get(row.quality_flag)
    if panel:
        notes.append(f"Cette observation appartient au {panel}, sans couverture exhaustive.")
    if row.destination == "Tanzanie":
        notes.append("Il s’agit d’une part publiée, pas d’un volume exact d’arrivées ; les parts ne sont pas renormalisées à 100 %.")
    if row.origin_name == "Scandinaves":
        notes.append("Scandinaves est traité comme un agrégat régional et non comme un pays. Sa composition exacte reste à vérifier.")
    if row.granularity == "institutional_category":
        notes.append("Cette observation correspond à une catégorie institutionnelle et non à un pays.")
    if row.destination == "Maurice" and row.origin_name in ["Reunion Island", "Réunion", "Reunion"]:
        notes.append("Réunion reste un marché distinct de France.")
    if row.destination == "Égypte":
        if row.granularity == "country":
            label = "Observation du marché États-Unis disponible dans le dataset"
        notes.append("La couverture égyptienne ne permet pas un classement global des marchés d’origine.")
        if row.granularity == "regional_aggregate":
            notes.append("Panneau régional fixé à 2019 ; parts des touristes et parts des nuitées restent distinctes.")
    if not notes:
        notes.append("L’observation décrit uniquement le périmètre publié ; ne pas additionner agrégats et composantes.")
    return (f"**{row.destination} · {row.origin_name} · {int(row.year)}**\n\n"
            f"{label} : **{value}.**\n\n"
            f"Granularité : **{granularity}**  \nCouverture : **{row.coverage_scope}**\n\n"
            + " ".join(notes))


def format_display_value(value: float, unit: str) -> str:
    """
    Convertit une valeur brute en texte lisible pour les tableaux.

    Important :
    - les parts restent stockées sous forme décimale dans le dataset ;
    - la multiplication par 100 est uniquement une transformation d'affichage ;
    - aucune valeur manquante n'est remplacée par zéro.
    """
    if pd.isna(value):
        return ""

    if unit == "share":
        return f"{value * 100:.1f} %"

    if unit == "persons":
        return f"{value:,.0f}".replace(",", " ")

    return f"{value:,.2f}".replace(",", " ")


def format_french_number(value, decimals: int = 2) -> str:
    """Formate un nombre pour l'interface sans modifier la valeur source."""
    if pd.isna(value):
        return "Non disponible"
    formatted = f"{float(value):,.{decimals}f}"
    return formatted.replace(",", " ").replace(".", ",")


def build_trend_display_table(data: pd.DataFrame, selected_layer: str, trend_view: str) -> pd.DataFrame:
    """Construit une version lisible des tableaux Tendances, distincte des exports."""
    display = data.copy()

    if "unit" in display.columns:
        display["unit"] = display["unit"].map(lambda x: UNIT_LABELS.get(x, x))

    if trend_view == "Variation annuelle":
        columns = [c for c in ["destination", "year", "value", "unit", "variation_pct"] if c in display.columns]
        display = display[columns]
        if "value" in display:
            display["value"] = display["value"].map(
                lambda x: format_french_number(x, 0) if selected_layer == "arrivals"
                else format_french_number(x, 2)
            )
        if "variation_pct" in display:
            display["variation_pct"] = display["variation_pct"].map(
                lambda x: "Non disponible" if pd.isna(x) else f"{format_french_number(x, 2)} %"
            )
        return display.rename(columns={
            "destination": "Destination", "year": "Année", "value": "Valeur",
            "unit": "Unité", "variation_pct": "Variation annuelle (%)",
        })

    columns = [c for c in ["destination", "year", "value", "unit"] if c in display.columns]
    display = display[columns]
    if "value" in display:
        decimals = 2 if selected_layer in ["receipts", "ratio"] else 0
        display["value"] = display["value"].map(lambda x: format_french_number(x, decimals))
    value_label = "Ratio recettes / arrivées" if selected_layer == "ratio" else "Valeur"
    return display.rename(columns={
        "destination": "Destination", "year": "Année", "value": value_label, "unit": "Unité",
    })


def build_comparison_display_table(data: pd.DataFrame, field: str, trend_unit: str) -> pd.DataFrame:
    """Simplifie le tableau de comparaison selon la dimension réellement choisie."""
    display = data.copy()
    if "destination" in display.columns:
        order_map = {name: idx for idx, name in enumerate(DESTINATION_ORDER)}
        display["_ordre"] = display["destination"].map(order_map).fillna(len(order_map))
        display = display.sort_values(["_ordre", "destination"]).drop(columns="_ordre")

    if field == "value":
        columns = [c for c in ["destination", "year", "value", "unit"] if c in display.columns]
        display = display[columns]
        if "value" in display:
            decimals = 0 if trend_unit == "Personnes" else 2
            display["value"] = display["value"].map(lambda x: format_french_number(x, decimals))
        if "unit" in display:
            display["unit"] = display["unit"].map(lambda x: UNIT_LABELS.get(x, x))
        return display.rename(columns={
            "destination": "Destination", "year": "Année",
            "value": "Valeur", "unit": "Unité",
        })

    selected_metric = "median_pct" if field == "median_pct" else "volatility_points"
    columns = [c for c in ["indicator", "destination", "observations", selected_metric, "annees_communes"]
               if c in display.columns]
    display = display[columns]
    if "indicator" in display:
        display["indicator"] = display["indicator"].map(
            {"arrivals": "Arrivées touristiques", "receipts": "Recettes touristiques"}
        ).fillna(display["indicator"])
    if selected_metric in display:
        display[selected_metric] = display[selected_metric].map(
            lambda x: format_french_number(x, 2)
        )
    return display.rename(columns={
        "indicator": "Indicateur",
        "destination": "Destination",
        "observations": "Observations",
        "median_pct": "Variation annuelle médiane (%)",
        "volatility_points": "Volatilité (points de pourcentage)",
        "annees_communes": "Années communes",
    })


def safe_filename(text: str) -> str:
    """
    Produit un fragment de nom de fichier simple pour les exports CSV.
    """
    cleaned = re.sub(r"[^\w\-]+", "_", str(text), flags=re.UNICODE)
    return cleaned.strip("_")


def ordered_destinations(values) -> list[str]:
    """
    Retourne les destinations dans l'ordre de présentation défini plus haut,
    puis ajoute d'éventuels libellés non prévus à la fin.
    """
    available = [str(v) for v in pd.Series(values).dropna().unique()]
    ordered = [d for d in DESTINATION_ORDER if d in available]
    extras = sorted(d for d in available if d not in ordered)
    return ordered + extras


# ==============================================================================
# 5. VUE D'ENSEMBLE
# ==============================================================================
# Cette partie est conçue pour une lecture immédiate lors d'une démonstration.
# Les informations plus techniques sont conservées dans un expander repliable.

st.subheader("Vue d'ensemble")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Observations",
        value=f"{len(df):,}".replace(",", " "),
    )

with col2:
    st.metric(
        label="Destinations",
        value=df["destination"].nunique(),
    )

with col3:
    st.metric(
        label="Dimensions du dataset",
        value=df["dataset_layer"].nunique(),
    )

displayed_destinations = ordered_destinations(df["destination"])

if displayed_destinations:
    if len(displayed_destinations) > 1:
        destination_text = (
            ", ".join(displayed_destinations[:-1])
            + " et "
            + displayed_destinations[-1]
        )
    else:
        destination_text = displayed_destinations[0]

    st.caption(f"Destinations étudiées : {destination_text}.")

# Encadré méthodologique visible dès l'ouverture.
st.markdown(
    f"""
    <div style="
        background-color: {CORP['panel']};
        color: {CORP['text']};
        border-left: 5px solid {CORP['accent']};
        padding: 14px 16px;
        border-radius: 8px;
        margin: 15px 0 25px 0;
        line-height: 1.5;
    ">
        <strong>Principe de lecture</strong><br>
        Le dashboard distingue trois dimensions : arrivées touristiques,
        recettes touristiques et provenance des touristes. Les valeurs manquantes
        restent manquantes et ne sont jamais remplacées par zéro. Les comparaisons
        de provenance respectent le périmètre propre à chaque source afin de ne pas
        créer une comparabilité artificielle.
    </div>
    """,
    unsafe_allow_html=True,
)

# Les contrôles de structure sont utiles pour le développement et la transparence,
# mais restent repliés pour ne pas surcharger la démonstration.
with st.expander("Contrôle technique du dataset"):
    st.write("#### Répartition des observations")

    layer_counts = (
        df["dataset_layer"]
        .value_counts()
        .rename_axis("Couche")
        .reset_index(name="Observations")
    )

    layer_counts["Couche"] = layer_counts["Couche"].replace(LAYER_LABELS)

    st.dataframe(
        layer_counts,
        width="stretch",
        hide_index=True,
    )

    st.write("#### Aperçu du dataset maître")
    st.caption(
        "Les 20 premières lignes sont conservées ici pour contrôler les colonnes, "
        "les unités et les niveaux de granularité."
    )

    # Copie dédiée à l'affichage : le dataset maître reste strictement inchangé.
    master_preview = df.head(20).copy()

    if "dataset_layer" in master_preview.columns:
        master_preview["dataset_layer"] = master_preview["dataset_layer"].map(
            lambda x: LAYER_LABELS.get(x, x)
        )
    if "granularity" in master_preview.columns:
        master_preview["granularity"] = master_preview["granularity"].map(
            lambda x: GRANULARITY_LABELS.get(x, x)
        )
    if "metric_type" in master_preview.columns:
        master_preview["metric_type"] = master_preview["metric_type"].map(
            lambda x: METRIC_TYPE_LABELS.get(x, x)
        )
    if "metric" in master_preview.columns:
        master_preview["metric"] = master_preview["metric"].map(
            lambda x: METRIC_LABELS.get(x, x)
        )
    if "unit" in master_preview.columns:
        master_preview["unit"] = master_preview["unit"].map(
            lambda x: UNIT_LABELS.get(x, x)
        )
    if "quality_flag" in master_preview.columns:
        master_preview["quality_flag"] = master_preview["quality_flag"].map(
            lambda x: QUALITY_FLAG_LABELS.get(x, x)
        )

    master_preview = master_preview.rename(
        columns={
            **COLUMN_LABELS,
            "iso3": "Code ISO-3",
            "origin_region": "Région d’origine",
            "metric": "Mesure",
        }
    )

    st.dataframe(
        master_preview,
        width="stretch",
        hide_index=True,
    )


# ==============================================================================
# 6. TABLEAU DE BORD — NAVIGATION PRINCIPALE
# ==============================================================================

st.markdown("---")
st.header("Tableau de bord")

# Les groupes restent accessibles quelle que soit la vue ouverte.
with st.sidebar:
    st.header("Filtres")
    with st.expander("Tendances", expanded=True):
        trend_destination_filters = st.container()
        trend_indicator_filters = st.container()
        trend_period_filters = st.container()
    origin_filters = st.expander("Provenance", expanded=True)
    map_filters = st.expander("Carte", expanded=True)

tab_trends, tab_origin, tab_map = st.tabs(
    ["Tendances", "Provenance", "Carte"]
)


# ==============================================================================
# ONGLET 1 — TENDANCES
# ==============================================================================
# Objectif :
# comparer l'évolution des arrivées ou des recettes pour une ou plusieurs
# destinations, sans convertir les valeurs manquantes en zéro.


with tab_trends:
    # Imports scoped to this view; the other views retain their existing behavior.
    import sys
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from src.indicators import (
        national_series, annual_variations, consecutive_segments, common_pre2020_summary,
    )

    st.subheader("Tendances nationales")
    selected_destinations = trend_destination_filters.multiselect(
        "Destinations", ordered_destinations(df["destination"]),
        default=ordered_destinations(df["destination"]), key="trend_destinations")
    trend_options = {
        "Arrivées touristiques internationales": ("arrivals", "Personnes"),
        "Recettes touristiques": ("receipts", "USD courants"),
    }
    indicator_label = trend_indicator_filters.selectbox(
        "Indicateur", list(trend_options), key="trend_indicator")
    selected_layer, trend_unit = trend_options[indicator_label]
    trends_df = national_series(df, selected_layer)
    year_min, year_max = int(trends_df.year.min()), int(trends_df.year.max())
    year_range = trend_period_filters.slider(
        "Période", min_value=year_min, max_value=year_max,
        value=(year_min, year_max), key="trend_year_range")
    st.caption(
        "Recettes et ratio en USD courants, sans correction d'inflation. Le ratio est agrégé. "
        "Les variations sont descriptives, sans causalité. Les absences ne sont jamais des zéros. "
        "Les données nationales s'arrêtent au plus tard en 2020 : aucune reprise post-Covid calculée.")

    analysis_tabs = st.tabs(["Évolution", "Variation annuelle", "Ratio recettes / arrivées", "Comparaison"])
    for analysis_index, analysis_tab in enumerate(analysis_tabs):
        with analysis_tab:
            selected_layer, trend_unit = trend_options[indicator_label]
            trend_view = ["Niveaux dans le temps", "Variation annuelle", "Niveaux dans le temps", "Comparaison des destinations"][analysis_index]
            if analysis_index == 2:
                selected_layer, trend_unit = "ratio", "USD courants par arrivée"
                st.caption("Le ratio combine arrivées et recettes : le filtre Indicateur ne s'applique pas ici. Ratio agrégé, ni dépense individuelle, ni rentabilité, ni qualité.")
            trends_df = national_series(df, selected_layer)
            applied_period = "2019 (niveaux) ; 1998–2019 (statistiques)" if analysis_index == 3 else f"{year_range[0]}–{year_range[1]}"
            applied_indicator = "Ratio recettes / arrivées" if analysis_index == 2 else indicator_label
            st.caption(f"Périmètre actif : {', '.join(selected_destinations)} | {applied_indicator} | {trend_unit} | {applied_period}.")
            if not selected_destinations:
                st.info("Aucune donnée disponible : sélectionnez une destination.")
            else:
                filtered_trends = trends_df.loc[
                    trends_df.destination.isin(selected_destinations)
                    & trends_df.year.between(*year_range)].copy()
                export_df = filtered_trends[["destination", "year", "value", "unit"]].copy()
                if trend_view == "Comparaison des destinations":
                    comparison_dimension = st.radio(
                        "Dimension comparée", ["Niveaux 2019", "Variation annuelle médiane pré-2020",
                                               "Volatilité pré-2020"], key="trend_comparison")
                    st.caption("Cette comparaison utilise son périmètre commun indiqué ci-dessous ; le filtre de période ne s'y applique pas.")
                    if comparison_dimension == "Niveaux 2019":
                        view_data = trends_df.loc[trends_df.destination.isin(selected_destinations) & trends_df.year.eq(2019)].copy()
                        field, axis_title = "value", trend_unit
                        st.write(f"**Niveaux nationaux — 2019 — {trend_unit}**")
                        export_df = view_data[["destination", "year", "value", "unit"]].copy()
                        if view_data.value.notna().sum() != len(selected_destinations):
                            st.warning("Données insuffisantes pour comparer toutes les destinations sélectionnées en 2019.")
                    elif selected_layer == "ratio":
                        view_data = pd.DataFrame()
                        st.info("La dynamique et la volatilité validées concernent les arrivées et les recettes. Sélectionnez l'un de ces indicateurs.")
                    else:
                        summary, common_years = common_pre2020_summary(df, DESTINATION_ORDER)
                        view_data = summary.loc[summary.indicator.eq(selected_layer) & summary.destination.isin(selected_destinations)].copy()
                        field = "median_pct" if comparison_dimension.startswith("Variation") else "volatility_points"
                        axis_title = "%" if field == "median_pct" else "Points de pourcentage"
                        if common_years:
                            st.write(f"**Années de variation communes : {', '.join(map(str, common_years))}**")
                            st.caption(
                                f"{len(common_years)} variations par série ; mêmes années pour arrivées et recettes. "
                                "Médiane annuelle distincte du CAGR ; volatilité = écart-type échantillonnal, sans prédiction de risque.")
                        view_data["annees_communes"] = ", ".join(map(str, common_years))
                        export_df = view_data.copy()
                    if not view_data.empty:
                        plot_data = view_data.loc[view_data[field].notna()]
                        if not plot_data.empty:
                            plot_data = plot_data.assign(display_dimension=f"{indicator_label} — {comparison_dimension}",
                                                         display_period="2019" if field == "value" else f"{min(common_years)}–{max(common_years)}",
                                                         display_unit=axis_title)
                            chart = alt.Chart(plot_data).mark_bar().encode(
                                y=alt.Y("destination:N", title="Destination", sort=DESTINATION_ORDER),
                                x=alt.X(f"{field}:Q", title=axis_title),
                                tooltip=[alt.Tooltip("destination:N", title="Destination"),
                                         alt.Tooltip("display_dimension:N", title="Dimension"),
                                         alt.Tooltip("display_period:N", title="Année" if field == "value" else "Période"),
                                         alt.Tooltip(f"{field}:Q", title="Valeur", format=",.2f"),
                                         alt.Tooltip("display_unit:N", title="Unité")]
                                        + ([alt.Tooltip("observations:Q", title="Nombre d’observations", format="d")] if field != "value" else []))
                            bar_selection = alt.selection_point(
                                name="comparison_bar", fields=["destination", "display_dimension", "display_period"],
                                on="click", toggle=False, clear="dblclick")
                            chart = chart.add_params(bar_selection).encode(
                                opacity=alt.condition(bar_selection, alt.value(1), alt.value(0.45)))
                            chart = chart.configure(locale={"number": FRENCH_NUMBER_LOCALE})
                            event = st.altair_chart(
                                chart, width="stretch", key="comparison_chart",
                                on_select="rerun", selection_mode=["comparison_bar"])
                            comment = build_comparison_comment(
                                event.get("selection", {}).get("comparison_bar", []), plot_data, field)
                            if comment:
                                with st.container(border=True):
                                    st.markdown("### Lecture du graphique")
                                    st.markdown(comment)
                            else:
                                st.caption("Cliquez sur une barre pour afficher son interprétation.")
                        else:
                            st.info("Données insuffisantes pour cette comparaison.")
                        comparison_display = build_comparison_display_table(
                            view_data, field, trend_unit
                        )
                        st.dataframe(comparison_display, width="stretch", hide_index=True)
                    else:
                        export_df = pd.DataFrame()
                else:
                    if trend_view == "Variation annuelle" and selected_layer == "ratio":
                        st.info("Les variations annuelles proposées concernent les arrivées ou les recettes, pas le ratio.")
                        export_df = pd.DataFrame()
                    else:
                        if trend_view == "Variation annuelle":
                            # Compute before period filtering so t-1 remains available at the left boundary.
                            changes = annual_variations(trends_df)
                            view_data = changes.loc[changes.destination.isin(selected_destinations) & changes.year.between(*year_range)].copy()
                            field, axis_title = "variation_pct", "Variation annuelle (%)"
                            export_df = view_data[["destination", "year", "value", "unit", "variation_pct"]].copy()
                            plot_data = view_data.loc[view_data[field].notna()].copy()
                            plot_data["periode"] = plot_data.year.eq(2020).map({True: "2020 — rupture exceptionnelle", False: "Autres années"})
                            if not plot_data.empty:
                                plot_data = plot_data.assign(display_indicator=indicator_label)
                                first_year, last_year = int(plot_data.year.min()), int(plot_data.year.max())
                                year_domain = ([first_year, last_year] if first_year != last_year
                                               else [first_year - 0.5, last_year + 0.5])
                                tick_step = max(1, (last_year - first_year + 6) // 7)
                                year_ticks = list(range(first_year, last_year + 1, tick_step))
                                if year_ticks[-1] != last_year:
                                    year_ticks.append(last_year)
                                chart = alt.Chart(plot_data).mark_circle(size=70).encode(
                                    x=alt.X("year:Q", title="Année",
                                            scale=alt.Scale(domain=year_domain, zero=False, nice=False),
                                            axis=alt.Axis(format="d", values=year_ticks)),
                                    y=alt.Y("variation_pct:Q", title=axis_title),
                                    color=alt.Color("destination:N", title="Destination", sort=DESTINATION_ORDER),
                                    shape=alt.Shape("periode:N", title="Période"),
                                    tooltip=[alt.Tooltip("destination:N", title="Destination"), alt.Tooltip("year:O", title="Année"),
                                             alt.Tooltip("display_indicator:N", title="Indicateur"),
                                             alt.Tooltip("variation_pct:Q", title="Variation annuelle (%)", format=".2f"),
                                             alt.Tooltip("periode:N", title="Période")])
                            st.caption("2020 : rupture exceptionnelle, identifiée séparément. Calcul uniquement entre années consécutives renseignées, avec une base strictement positive.")
                        else:
                            view_data = filtered_trends
                            plot_data = consecutive_segments(view_data)
                            if not plot_data.empty:
                                plot_data = plot_data.assign(display_indicator=applied_indicator,
                                                             display_unit="USD courants / arrivée" if selected_layer == "ratio" else trend_unit)
                                chart = alt.Chart(plot_data).mark_line(point=True).encode(
                                    x=alt.X("year:Q", title="Année", axis=alt.Axis(format="d")),
                                    y=alt.Y("value:Q", title=trend_unit),
                                    color=alt.Color("destination:N", title="Destination", sort=DESTINATION_ORDER),
                                    detail="segment:N", order="year:Q",
                                    tooltip=[alt.Tooltip("destination:N", title="Destination"), alt.Tooltip("year:O", title="Année"),
                                             alt.Tooltip("display_indicator:N", title="Indicateur"),
                                             alt.Tooltip("value:Q", title="Ratio recettes / arrivées" if selected_layer == "ratio" else "Valeur", format=",.2f"),
                                             alt.Tooltip("display_unit:N", title="Unité")])
                        if not plot_data.empty:
                            if trend_view == "Variation annuelle":
                                point_selection = alt.selection_point(
                                    name="annual_change_point",
                                    fields=["destination", "year", "display_indicator"],
                                    on="click", toggle=False, clear="dblclick")
                                chart = chart.add_params(point_selection).encode(
                                    opacity=alt.condition(point_selection, alt.value(1), alt.value(0.45)))
                                chart = chart.configure(locale={"number": FRENCH_NUMBER_LOCALE})
                                event = st.altair_chart(
                                    chart, width="stretch", key="annual_change_chart",
                                    on_select="rerun", selection_mode=["annual_change_point"])
                                comment = build_annual_change_comment(
                                    event.get("selection", {}).get("annual_change_point", []), plot_data, indicator_label)
                                if comment:
                                    with st.container(border=True):
                                        st.markdown("### Lecture du graphique")
                                        st.markdown(comment)
                                else:
                                    st.caption("Cliquez sur un point pour afficher son interprétation.")
                            else:
                                level_selection = alt.selection_point(
                                    name="trend_level_point",
                                    fields=["destination", "year", "display_indicator"],
                                    on="click", toggle=False, clear="dblclick")
                                chart = chart.add_params(level_selection).encode(
                                    opacity=alt.condition(level_selection, alt.value(1), alt.value(0.45)))
                                chart = chart.configure(locale={"number": FRENCH_NUMBER_LOCALE})
                                event = st.altair_chart(
                                    chart, width="stretch", key=f"trend_level_chart_{selected_layer}",
                                    on_select="rerun", selection_mode=["trend_level_point"])
                                comment = build_level_comment(
                                    event.get("selection", {}).get("trend_level_point", []),
                                    view_data, applied_indicator, selected_layer)
                                if comment:
                                    with st.container(border=True):
                                        st.markdown("### Lecture du graphique")
                                        st.markdown(comment)
                                else:
                                    st.caption("Cliquez sur un point pour afficher son interprétation.")
                        else:
                            st.info("Aucune valeur calculable pour cette sélection.")
                        trends_display = build_trend_display_table(
                            export_df, selected_layer, trend_view
                        )
                        st.dataframe(trends_display, width="stretch", hide_index=True)
                if not export_df.empty:
                    # Enrich only the CSV; displayed tables and calculations are unchanged.
                    export_metadata = ["metric", "metric_type", "source_name", "source_reference",
                                       "quality_flag", "coverage_scope"]
                    if trend_view == "Comparaison des destinations" and comparison_dimension != "Niveaux 2019":
                        export_df = export_df[["destination", "indicator", field, "observations", "annees_communes"]].copy()
                        export_df["unit"] = "%" if field == "median_pct" else "percentage_points"
                        export_df["reference_start_year"] = min(common_years) if common_years else None
                        export_df["reference_end_year"] = max(common_years) if common_years else None
                        reference_years = set(common_years) | {year - 1 for year in common_years}
                        reference = df.loc[df.dataset_layer.eq(selected_layer) & df.year.isin(reference_years)]
                        metadata = reference.groupby("destination")[export_metadata].agg(
                            lambda values: " | ".join(sorted(set(values.dropna().astype(str))))).reset_index()
                        export_df = export_df.merge(metadata, on="destination", how="left", validate="one_to_one")
                    elif selected_layer == "ratio":
                        export_df = trends_df.merge(
                            export_df[["destination", "year"]], on=["destination", "year"],
                            how="inner", validate="one_to_one"
                        )[["destination", "year", "receipts", "arrivals", "value", "unit"]].rename(
                            columns={"value": "ratio_receipts_per_arrival"})
                        export_df["indicator"] = "receipts_per_arrival"
                        for source_layer in ["arrivals", "receipts"]:
                            metadata = df.loc[df.dataset_layer.eq(source_layer),
                                              ["destination", "year"] + export_metadata].rename(
                                columns={column: f"{column}_{source_layer}" for column in export_metadata})
                            export_df = export_df.merge(metadata, on=["destination", "year"], how="left", validate="one_to_one")
                    else:
                        export_df = export_df.copy()
                        export_df["indicator"] = selected_layer
                        metadata = df.loc[df.dataset_layer.eq(selected_layer),
                                          ["destination", "year"] + export_metadata]
                        export_df = export_df.merge(metadata, on=["destination", "year"], how="left", validate="one_to_one")
                        if "variation_pct" in export_df:
                            export_df["variation_unit"] = "%"
                    st.download_button(
                        "Télécharger les données affichées en CSV",
                        data=export_df.to_csv(index=False).encode("utf-8"),
                        file_name=f"tendances_{selected_layer}_{safe_filename(trend_view)}.csv",
                        mime="text/csv", key=f"download_trends_{analysis_index}")

# ==============================================================================
# ONGLET 2 — PROVENANCE
# ==============================================================================
# Objectif :
# montrer les marchés d'origine disponibles sans forcer une comparaison entre
# des sources qui n'ont pas le même périmètre, la même granularité ou la même
# unité de mesure.


with tab_origin:
    st.subheader("Provenance des visiteurs")
    provenance_df = df.loc[df.dataset_layer.eq("provenance")].copy()
    selected_origin_destination = origin_filters.selectbox(
        "Destination", ordered_destinations(provenance_df.destination), key="origin_destination")
    destination_df = provenance_df.loc[provenance_df.destination.eq(selected_origin_destination)].copy()
    origin_years = sorted(destination_df.year.unique(), reverse=True)
    if st.session_state.get("origin_year") not in origin_years:
        st.session_state["origin_year"] = origin_years[0]
    selected_origin_year = origin_filters.selectbox(
        "Année", origin_years, key="origin_year")
    origin_filtered = destination_df.loc[destination_df.year.eq(selected_origin_year)].copy()
    origin_categories = ["Toutes les catégories"] + sorted(destination_df.granularity.unique())
    if st.session_state.get("origin_category") not in origin_categories:
        st.session_state["origin_category"] = origin_categories[0]
    selected_origin_category = origin_filters.selectbox(
        "Catégorie", origin_categories, key="origin_category")
    if selected_origin_category != origin_categories[0]:
        origin_filtered = origin_filtered.loc[origin_filtered.granularity.eq(selected_origin_category)].copy()
    origin_group_columns = ["granularity", "metric_type", "unit", "coverage_scope"]
    st.caption(f"Périmètre actif : {selected_origin_destination} | {selected_origin_year} | {selected_origin_category}.")
    st.caption(
        "Les marchés ne sont comparés qu'au sein d'une même année, granularité, mesure et couverture. "
        "Aucun classement entre destinations. Une valeur absente n'est pas un zéro.")
    st.write("### Couverture de la sélection")
    origin_coverage = origin_filtered.groupby(
        origin_group_columns + ["quality_flag"], dropna=False).agg(
        lignes=("value", "size"), valeurs_renseignees=("value", "count"),
        valeurs_absentes=("value", lambda s: int(s.isna().sum()))).reset_index()
    origin_coverage.insert(0, "year", selected_origin_year)
    origin_coverage.insert(0, "destination", selected_origin_destination)

    # Version lisible pour l'interface : les données techniques restent inchangées.
    origin_coverage_display = origin_coverage.copy()
    origin_coverage_display["granularity"] = origin_coverage_display["granularity"].map(
        lambda x: GRANULARITY_LABELS.get(x, x)
    )
    origin_coverage_display["metric_type"] = origin_coverage_display["metric_type"].map(
        lambda x: METRIC_TYPE_LABELS.get(x, x)
    )
    origin_coverage_display["unit"] = origin_coverage_display["unit"].map(
        lambda x: UNIT_LABELS.get(x, x)
    )
    origin_coverage_display["quality_flag"] = origin_coverage_display["quality_flag"].map(
        lambda x: QUALITY_FLAG_LABELS.get(x, x)
    )
    origin_coverage_display = origin_coverage_display.rename(
        columns={
            **COLUMN_LABELS,
            "lignes": "Lignes",
            "valeurs_renseignees": "Valeurs renseignées",
            "valeurs_absentes": "Valeurs absentes",
        }
    )
    st.dataframe(origin_coverage_display, width="stretch", hide_index=True)
    if selected_origin_destination == "Tunisie":
        tunisian_missing = destination_df.loc[destination_df.value.isna()]
        st.caption(
            f"{len(tunisian_missing)} valeurs absentes dans la provenance tunisienne ; "
            "les absences 2017–2018 restent non vérifiées et ne sont jamais remplacées par zéro.")
        if not tunisian_missing.empty:
            missing_coverage = tunisian_missing.groupby(
                ["year", "quality_flag"]
            ).size().reset_index(name="valeurs_absentes")
            missing_coverage_display = missing_coverage.copy()
            missing_coverage_display["quality_flag"] = missing_coverage_display["quality_flag"].map(
                lambda x: QUALITY_FLAG_LABELS.get(x, x)
            )
            missing_coverage_display = missing_coverage_display.rename(
                columns={
                    "year": "Année",
                    "quality_flag": "Qualité",
                    "valeurs_absentes": "Valeurs absentes",
                }
            )
            st.dataframe(missing_coverage_display, width="stretch", hide_index=True)
    if selected_origin_destination == "Tanzanie":
        st.info(
            "Top 15 de l'Exit Survey : parts publiées, susceptibles de totaliser moins de 100 %. "
            "Aucune renormalisation et aucune conversion en volumes.")
    if selected_origin_destination == "Égypte":
        st.warning(
            "Un seul marché pays est vérifié : il ne représente pas nécessairement le principal marché. "
            "La couverture ne permet aucun classement complet des marchés égyptiens.")
        st.caption(
            "Le marché pays suit l'année sélectionnée. Le panneau régional complémentaire est fixé à 2019 ; "
            "parts des touristes et parts des nuitées sont distinctes.")

    def render_origin_groups(table, heading):
        st.write(heading)
        if table.empty:
            st.info("Aucune observation publiée pour ce périmètre.")
            return
        # Quality is included in grouping: missing rows remain visible in their own group.
        for identity, group in table.groupby(origin_group_columns + ["quality_flag"], dropna=False, sort=False):
            granularity, metric_type, unit, scope, quality = identity

            granularity_label = GRANULARITY_LABELS.get(granularity, granularity)
            metric_type_label = METRIC_TYPE_LABELS.get(metric_type, metric_type)
            unit_label = UNIT_LABELS.get(unit, unit)
            quality_label = QUALITY_FLAG_LABELS.get(quality, quality)

            st.write(f"**{granularity_label} — {metric_type_label} — {unit_label}**")
            st.caption(
                f"Année(s) : {', '.join(map(str, sorted(group.year.unique())))} "
                f"| Couverture : {scope} | Qualité : {quality_label}"
            )
            if quality in ["exact_panel18", "exact_top30", "exact_main7", "survey_share_top15"]:
                st.caption("Panel partiel / Top-N : un classement décrit uniquement les marchés publiés, sans exhaustivité nationale.")
            else:
                st.caption("Périmètre publié uniquement ; ne pas additionner agrégats et composantes.")

            available = group.loc[group.value.notna()].copy()
            # Only homogeneous country or regional categories are ranked.
            chart_allowed = granularity in ["country", "regional_aggregate"]
            if not available.empty and chart_allowed:
                available["display_value"] = available.value * 100 if unit == "share" else available.value
                value_label = "Part publiée (%)" if unit == "share" else "Personnes" if unit == "persons" else unit_label
                available = available.assign(
                    display_unit="part (%)" if unit == "share" else "personnes",
                    display_granularity=GRANULARITY_LABELS.get(granularity, granularity)
                )
                chart = alt.Chart(available).mark_bar().encode(
                    x=alt.X("display_value:Q", title=value_label),
                    y=alt.Y("origin_name:N", title="Catégorie publiée", sort="-x"),
                    tooltip=[
                        alt.Tooltip("destination:N", title="Destination"),
                        alt.Tooltip("origin_name:N", title="Origine"),
                        alt.Tooltip("year:O", title="Année"),
                        alt.Tooltip("display_value:Q", title="Valeur", format=",.2f"),
                        alt.Tooltip("display_unit:N", title="Unité"),
                        alt.Tooltip("display_granularity:N", title="Granularité"),
                        alt.Tooltip("coverage_scope:N", title="Couverture"),
                    ]
                ).properties(height=max(180, min(800, len(available) * 28)))
                origin_selection = alt.selection_point(
                    name="origin_bar", fields=ORIGIN_SELECTION_FIELDS,
                    on="click", toggle=False, clear="dblclick")
                chart = chart.add_params(origin_selection).encode(
                    opacity=alt.condition(origin_selection, alt.value(1), alt.value(0.45)))
                chart = chart.configure(locale={"number": FRENCH_NUMBER_LOCALE})
                event = st.altair_chart(
                    chart, width="stretch",
                    key=f"origin_chart_{heading}_{selected_origin_destination}_{identity!r}",
                    on_select="rerun", selection_mode=["origin_bar"])
                comment = build_origin_comment(
                    event.get("selection", {}).get("origin_bar", []), available)
                if comment:
                    with st.container(border=True):
                        st.markdown("### Lecture du graphique")
                        st.markdown(comment)
                else:
                    st.caption("Cliquez sur une barre pour afficher son interprétation.")

            display_group = group[[
                "destination", "year", "origin_name", "granularity", "metric_type",
                "value", "unit", "coverage_scope", "quality_flag", "source_name", "source_reference", "notes"
            ]].copy()
            # No global sort across incompatible categories or units.
            display_group["Valeur affichée"] = display_group.apply(
                lambda row: "Non disponible" if pd.isna(row.value) else format_display_value(row.value, row.unit), axis=1)

            display_group["granularity"] = display_group["granularity"].map(
                lambda x: GRANULARITY_LABELS.get(x, x))
            display_group["metric_type"] = display_group["metric_type"].map(
                lambda x: METRIC_TYPE_LABELS.get(x, x))
            display_group["unit"] = display_group["unit"].map(
                lambda x: UNIT_LABELS.get(x, x))
            display_group["quality_flag"] = display_group["quality_flag"].map(
                lambda x: QUALITY_FLAG_LABELS.get(x, x))
            display_group = display_group.rename(columns=COLUMN_LABELS)

            st.dataframe(display_group, width="stretch", hide_index=True)

    if selected_origin_destination == "Égypte":
        render_origin_groups(origin_filtered.loc[origin_filtered.granularity.eq("country")],
                             "### Marché pays vérifié — année sélectionnée")
        egypt_regions = destination_df.loc[
            destination_df.year.eq(2019) & destination_df.granularity.eq("regional_aggregate")
            & destination_df.unit.eq("share")
            & destination_df.metric_type.isin(["regional_tourist_share", "regional_tourist_nights_share"])].copy()
        if selected_origin_category not in [origin_categories[0], "regional_aggregate"]:
            egypt_regions = egypt_regions.iloc[:0].copy()
        render_origin_groups(egypt_regions, "### Parts régionales — 2019 uniquement")
    else:
        render_origin_groups(origin_filtered, "### Données par groupes comparables")

    export_origin_columns = [
        "destination", "year", "origin_name", "origin_region", "granularity",
        "metric_type", "value", "unit", "coverage_scope", "quality_flag",
        "source_name", "source_reference", "notes",
    ]
    st.download_button(
        "Télécharger la sélection annuelle de provenance en CSV",
        data=origin_filtered[export_origin_columns].to_csv(index=False).encode("utf-8"),
        file_name=f"provenance_{safe_filename(selected_origin_destination)}_{selected_origin_year}.csv",
        mime="text/csv", key="download_origin")
    if selected_origin_destination == "Égypte" and not egypt_regions.empty:
        st.download_button(
            "Télécharger les parts régionales de 2019 en CSV",
            data=egypt_regions[export_origin_columns].to_csv(index=False).encode("utf-8"),
            file_name="provenance_egypte_regions_2019.csv", mime="text/csv", key="download_origin_regions")


# ==============================================================================
# ONGLET 3 — CARTE
# ==============================================================================
# Objectif :
# fournir une lecture géographique des arrivées ou des recettes pour une année
# donnée. Les codes ISO-3 sont utilisés pour fiabiliser la reconnaissance des
# sept destinations, notamment Maurice (MUS).


with tab_map:
    st.subheader("Comparaison géographique nationale")
    map_indicator_label = map_filters.selectbox(
        "Indicateur cartographié",
        ["Arrivées touristiques internationales", "Recettes touristiques"],
        key="map_indicator")
    map_layer = {"Arrivées touristiques internationales": "arrivals",
                 "Recettes touristiques": "receipts"}[map_indicator_label]
    map_unit = "persons" if map_layer == "arrivals" else "current_USD"
    map_unit_label = "Personnes" if map_layer == "arrivals" else "USD courants"
    map_source = df.loc[
        df.dataset_layer.eq(map_layer) & df.granularity.eq("destination_total")
        & df.metric_type.eq("destination_total") & df.unit.eq(map_unit)].copy()
    if map_source.duplicated(["destination", "year"]).any():
        st.error("Clés nationales dupliquées : carte non disponible.")
    elif map_source.empty:
        st.info("Aucune donnée nationale disponible.")
    else:
        map_years = sorted(map_source.year.unique(), reverse=True)
        map_year = map_filters.selectbox(
            "Année", map_years, index=map_years.index(2019) if 2019 in map_years else 0,
            key="map_year")
        # Reindex only the destination perimeter; no observed value is filled.
        map_df = map_source.loc[map_source.year.eq(map_year), [
            "destination", "iso3", "year", "dataset_layer", "value", "unit",
            "source_name", "quality_flag"
        ]].set_index("destination").reindex(DESTINATION_ORDER).reset_index()
        map_df["iso3"] = map_df.destination.map(COUNTRY_ISO_MAP)
        map_df["year"] = map_year
        map_df["dataset_layer"] = map_layer
        map_df["unit"] = map_unit
        mapped_df = map_df.loc[map_df.value.notna() & map_df.iso3.notna()].copy()
        missing_map_destinations = map_df.loc[map_df.value.isna(), "destination"].tolist()
        st.caption(
            f"Périmètre actif : {map_indicator_label} | {map_year} | {map_unit_label} | "
            f"{len(mapped_df)}/{len(map_df)} destinations couvertes.")
        st.caption("Sans valeur disponible : " + (", ".join(missing_map_destinations) or "aucune") + ".")
        st.caption(
            "Même année pour toutes les destinations. Les absences restent non disponibles, jamais égales à zéro. "
            "Les recettes sont nominales, sans correction d'inflation.")
        if not HAS_PLOTLY:
            st.error("Plotly n'est pas disponible : consultez le tableau et l'export.")
        elif mapped_df.empty:
            st.info("Aucune donnée cartographiable pour cette sélection.")
        else:
            fig = px.choropleth(
                mapped_df.assign(display_indicator=map_indicator_label, display_unit=map_unit_label), locations="iso3", locationmode="ISO-3", color="value",
                scope="africa", hover_name="destination", custom_data=["destination", "year", "source_name", "unit"],
                hover_data={"value": ":,.0f", "year": True, "display_unit": True, "display_indicator": True,
                            "source_name": True, "iso3": False},
                labels={"destination": "Destination", "year": "Année", "value": "Valeur",
                        "display_unit": "Unité", "display_indicator": "Indicateur", "source_name": "Source"},
                title=f"{map_indicator_label} — {map_year} — {map_unit_label}",
                color_continuous_scale=[CORP["panel"], CORP["accent"]])
            fig.update_layout(
                margin=dict(l=10, r=10, t=70, b=10),
                paper_bgcolor=CORP["bg"], plot_bgcolor=CORP["bg"],
                font=dict(color=CORP["text"], size=13),
                title=dict(x=0.01, xanchor="left", font=dict(color=CORP["text"], size=20)))
            fig.update_geos(bgcolor=CORP["bg"], showcoastlines=True, showland=True)
            map_event = st.plotly_chart(
                fig, width="stretch", key="national_map_chart",
                on_select="rerun", selection_mode="points")
            map_points = []
            if map_event and getattr(map_event, "selection", None):
                map_points = list(getattr(map_event.selection, "points", []) or [])
            map_comment = build_map_comment(
                map_points, mapped_df, map_indicator_label, map_unit_label)
            if map_comment:
                with st.container(border=True):
                    st.markdown("### Lecture de la carte")
                    st.markdown(map_comment)
            else:
                st.caption("Cliquez sur une destination colorée pour afficher sa lecture.")
        st.write("### Données du périmètre cartographique")
        # Copie dédiée à l'affichage : la carte, les calculs et l'export restent inchangés.
        map_display = map_df[["destination", "year", "value", "unit", "source_name", "quality_flag"]].copy()

        # Valeurs lisibles au format français, sans modifier les données numériques sources.
        map_display["value"] = map_display["value"].map(
            lambda x: "Non disponible" if pd.isna(x) else format_french_number(x, 0)
        )
        map_display["unit"] = map_display["unit"].map(
            lambda x: UNIT_LABELS.get(x, x)
        )
        map_display["quality_flag"] = map_display["quality_flag"].map(
            lambda x: QUALITY_FLAG_LABELS.get(x, x)
        )
        map_display = map_display.rename(
            columns={
                "destination": "Destination",
                "year": "Année",
                "value": "Valeur",
                "unit": "Unité",
                "source_name": "Source",
                "quality_flag": "Qualité",
            }
        )
        st.dataframe(map_display, width="stretch", hide_index=True)
        map_export = map_df.rename(columns={"dataset_layer": "indicator"}).copy()
        map_csv = map_export.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Télécharger les données du périmètre en CSV", data=map_csv,
            file_name=f"carte_{map_layer}_{map_year}.csv", mime="text/csv", key="download_map")
