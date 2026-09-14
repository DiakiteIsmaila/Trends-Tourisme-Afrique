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

        html,
        body,
        [class*="css"],
        .stApp,
        .stApp p,
        .stApp span,
        .stApp label,
        .stApp li,
        .stApp div {{
            color: {CORP["text"]};
        }}


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

        [data-baseweb="select"] > div {{
            background-color: #ffffff !important;
            color: {CORP["text"]} !important;
        }}

        [data-baseweb="select"] span,
        [data-baseweb="select"] div {{
            color: {CORP["text"]} !important;
        }}

        [data-baseweb="input"] input {{
            color: {CORP["text"]} !important;
            background-color: #ffffff !important;
        }}


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
    "tourist_arrivals": "Arrivées touristiques",
    "regional_tourist_share": "Part des touristes",
    "regional_tourist_nights_share": "Part des nuitées",
}


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

    st.dataframe(
        df.head(20),
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
        "Ratio recettes / arrivées": ("ratio", "USD courants par arrivée"),
    }
    indicator_label = trend_indicator_filters.selectbox(
        "Indicateur", list(trend_options), key="trend_indicator")
    selected_layer, trend_unit = trend_options[indicator_label]
    trend_view = trend_indicator_filters.selectbox(
        "Vue", ["Niveaux dans le temps", "Variation annuelle", "Comparaison des destinations"],
        key="trend_view")
    trends_df = national_series(df, selected_layer)
    year_min, year_max = int(trends_df.year.min()), int(trends_df.year.max())
    year_range = trend_period_filters.slider(
        "Période", min_value=year_min, max_value=year_max,
        value=(year_min, year_max), key="trend_year_range")
    st.caption(
        f"Périmètre actif : {', '.join(selected_destinations) or 'Aucune destination sélectionnée'} | "
        f"{indicator_label} | {trend_unit} | {year_range[0]}–{year_range[1]}.")
    st.caption(
        "Recettes et ratio en USD courants, sans correction d'inflation. Le ratio est agrégé. "
        "Les variations sont descriptives, sans causalité. Les absences ne sont jamais des zéros. "
        "Les données nationales s'arrêtent au plus tard en 2020 : aucune reprise post-Covid calculée.")

    if not selected_destinations:
        st.info("Aucune donnée disponible : sélectionnez une destination.")
    else:
        filtered_trends = trends_df.loc[
            trends_df.destination.isin(selected_destinations)
            & trends_df.year.between(*year_range)].copy()
        export_df = filtered_trends[["destination", "year", "value", "unit"]].copy()
        if trend_view == "Comparaison des destinations":
            comparison_dimension = trend_indicator_filters.selectbox(
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
                summary, common_years = common_pre2020_summary(df, selected_destinations)
                view_data = summary.loc[summary.indicator.eq(selected_layer)].copy()
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
                    chart = alt.Chart(plot_data).mark_bar().encode(
                        y=alt.Y("destination:N", title="Destination", sort="-x"),
                        x=alt.X(f"{field}:Q", title=axis_title),
                        tooltip=["destination:N", alt.Tooltip(f"{field}:Q", format=",.2f")])
                    st.altair_chart(chart, width="stretch")
                else:
                    st.info("Données insuffisantes pour cette comparaison.")
                st.dataframe(view_data, width="stretch", hide_index=True)
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
                        chart = alt.Chart(plot_data).mark_circle(size=70).encode(
                            x=alt.X("year:Q", title="Année de fin", axis=alt.Axis(format="d")),
                            y=alt.Y("variation_pct:Q", title=axis_title),
                            color=alt.Color("destination:N", title="Destination"),
                            shape=alt.Shape("periode:N", title="Période"),
                            tooltip=["destination:N", "year:O", "periode:N", alt.Tooltip("variation_pct:Q", format=".2f")])
                    st.caption("2020 : rupture exceptionnelle, identifiée séparément. Calcul uniquement entre années consécutives renseignées, avec une base strictement positive.")
                else:
                    view_data = filtered_trends
                    plot_data = consecutive_segments(view_data)
                    if not plot_data.empty:
                        chart = alt.Chart(plot_data).mark_line(point=True).encode(
                            x=alt.X("year:Q", title="Année", axis=alt.Axis(format="d")),
                            y=alt.Y("value:Q", title=trend_unit),
                            color=alt.Color("destination:N", title="Destination"),
                            detail="segment:N", order="year:Q",
                            tooltip=["destination:N", "year:O", alt.Tooltip("value:Q", format=",.2f"), "unit:N"])
                if not plot_data.empty:
                    st.altair_chart(chart, width="stretch")
                else:
                    st.info("Aucune valeur calculable pour cette sélection.")
                st.dataframe(export_df, width="stretch", hide_index=True)
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
                mime="text/csv", key="download_trends")


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
    selected_origin_year = origin_filters.selectbox(
        "Année", sorted(destination_df.year.unique(), reverse=True), key="origin_year")
    origin_filtered = destination_df.loc[destination_df.year.eq(selected_origin_year)].copy()
    origin_group_columns = ["granularity", "metric_type", "unit", "coverage_scope"]
    st.caption(f"Périmètre actif : {selected_origin_destination} | {selected_origin_year}.")
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
    st.dataframe(origin_coverage, width="stretch", hide_index=True)
    if selected_origin_destination == "Tunisie":
        tunisian_missing = destination_df.loc[destination_df.value.isna()]
        st.caption(
            f"{len(tunisian_missing)} valeurs absentes dans la provenance tunisienne ; "
            "les absences 2017–2018 restent non vérifiées (missing_unverified), jamais remplacées par zéro.")
        if not tunisian_missing.empty:
            missing_coverage = tunisian_missing.groupby(["year", "quality_flag"]).size().reset_index(name="valeurs_absentes")
            st.dataframe(missing_coverage, width="stretch", hide_index=True)
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
            st.write(f"**{granularity} — {metric_type} — {unit}**")
            st.caption(f"Année(s) : {', '.join(map(str, sorted(group.year.unique())))} | Couverture : {scope} | Qualité : {quality}")
            if quality in ["exact_panel18", "exact_top30", "exact_main7", "survey_share_top15"]:
                st.caption("Panel partiel / Top-N : un classement décrit uniquement les marchés publiés, sans exhaustivité nationale.")
            else:
                st.caption("Périmètre publié uniquement ; ne pas additionner agrégats et composantes.")
            available = group.loc[group.value.notna()].copy()
            # Only homogeneous country or regional categories are ranked.
            chart_allowed = granularity in ["country", "regional_aggregate"]
            if not available.empty and chart_allowed:
                available["display_value"] = available.value * 100 if unit == "share" else available.value
                value_label = "Part publiée (%)" if unit == "share" else "Personnes" if unit == "persons" else unit
                chart = alt.Chart(available).mark_bar().encode(
                    x=alt.X("display_value:Q", title=value_label),
                    y=alt.Y("origin_name:N", title="Catégorie publiée", sort="-x"),
                    tooltip=["origin_name:N", "year:O", alt.Tooltip("display_value:Q", title=value_label, format=",.2f"),
                             "metric_type:N", "coverage_scope:N", "quality_flag:N"]
                ).properties(height=max(180, min(800, len(available) * 28)))
                st.altair_chart(chart, width="stretch")
            display_group = group[[
                "destination", "year", "origin_name", "granularity", "metric_type",
                "value", "unit", "coverage_scope", "quality_flag", "source_name", "source_reference", "notes"
            ]].copy()
            # No global sort across incompatible categories or units.
            display_group["Valeur affichée"] = display_group.apply(
                lambda row: "Non disponible" if pd.isna(row.value) else format_display_value(row.value, row.unit), axis=1)
            st.dataframe(display_group, width="stretch", hide_index=True)

    if selected_origin_destination == "Égypte":
        render_origin_groups(origin_filtered.loc[origin_filtered.granularity.eq("country")],
                             "### Marché pays vérifié — année sélectionnée")
        egypt_regions = destination_df.loc[
            destination_df.year.eq(2019) & destination_df.granularity.eq("regional_aggregate")
            & destination_df.unit.eq("share")
            & destination_df.metric_type.isin(["regional_tourist_share", "regional_tourist_nights_share"])].copy()
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
                mapped_df, locations="iso3", locationmode="ISO-3", color="value",
                scope="africa", hover_name="destination",
                hover_data={"value": ":,.0f", "year": True, "unit": True,
                            "source_name": True, "quality_flag": True, "iso3": False},
                labels={"value": map_unit_label, "unit": "Unité"},
                title=f"{map_indicator_label} — {map_year} — {map_unit_label}",
                color_continuous_scale=[CORP["panel"], CORP["accent"]])
            fig.update_layout(
                margin=dict(l=10, r=10, t=70, b=10),
                paper_bgcolor=CORP["bg"], plot_bgcolor=CORP["bg"],
                font=dict(color=CORP["text"], size=13),
                title=dict(x=0.01, xanchor="left", font=dict(color=CORP["text"], size=20)))
            fig.update_geos(bgcolor=CORP["bg"], showcoastlines=True, showland=True)
            st.plotly_chart(fig, width="stretch")
        st.write("### Données du périmètre cartographique")
        map_display = map_df[["destination", "year", "value", "unit", "source_name", "quality_flag"]].copy()
        st.dataframe(map_display, width="stretch", hide_index=True)
        map_export = map_df.rename(columns={"dataset_layer": "indicator"}).copy()
        map_csv = map_export.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Télécharger les données du périmètre en CSV", data=map_csv,
            file_name=f"carte_{map_layer}_{map_year}.csv", mime="text/csv", key="download_map")
