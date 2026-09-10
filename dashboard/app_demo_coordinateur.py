from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st
import altair as alt
try:
    import plotly.express as px
    HAS_PLOTLY = True
except Exception:
    HAS_PLOTLY = False

# ==============================================================================
# CONFIGURATION DE LA PAGE
# ==============================================================================

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
# THÈME CORPORATE GAEA21
# ==============================================================================

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

    /* Fond général */
    .stApp {{
        background-color: {CORP["bg"]};
        color: {CORP["text"]};
    }}

    /* Barre latérale */
    section[data-testid="stSidebar"] > div:first-child {{
        background-color: {CORP["panel"]} !important;
    }}

    /* Conteneur principal */
    .block-container {{
        background: transparent;
    }}

    /* Texte des onglets */
    .stTabs [role="tablist"] button[role="tab"] {{
        color: {CORP["text"]} !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }}

    /* Onglet sélectionné */
    .stTabs [role="tablist"] button[aria-selected="true"] {{
        color: {CORP["accent"]} !important;
        border-bottom: 4px solid {CORP["accent"]} !important;
        font-weight: 700 !important;
    }}

    /* Amélioration de la visibilité au survol */
    .stTabs [role="tablist"] button[role="tab"]:hover {{
        color: {CORP["accent"]} !important;
    }}


    /* Contraste des indicateurs KPI */
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricLabel"] div,
    [data-testid="stMetricValue"] div {{
        color: {CORP["text"]} !important;
    }}

    /* Harmonisation du texte courant dans la page principale */
    .stApp p, .stApp label {{
        color: {CORP["text"]};
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# CHEMIN DU DATASET
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "final"
    / "dataset_maitre_trends_tourisme_afrique.csv"
)


# ==============================================================================
# CHARGEMENT DES DONNÉES
# ==============================================================================

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """
    Charge le dataset maître Trends.
    """
    return pd.read_csv(path)


if not DATA_PATH.exists():
    st.error(f"Dataset introuvable : {DATA_PATH}")
    st.stop()

df = load_data(DATA_PATH)


# ==============================================================================
# VUE D’ENSEMBLE DU DATASET
# ==============================================================================
# Cette section présente uniquement les informations utiles à la lecture du
# dashboard. Les contrôles plus techniques restent accessibles dans un expander
# afin de ne pas surcharger la page principale lors d’une démonstration.

st.subheader("Vue d'ensemble")

# Trois indicateurs synthétiques permettent de vérifier immédiatement la taille
# et le périmètre du dataset maître.
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Observations",
        value=f"{len(df):,}".replace(",", " ")
    )

with col2:
    st.metric(
        label="Destinations",
        value=df["destination"].nunique()
    )

with col3:
    st.metric(
        label="Dimensions analysées",
        value=df["dataset_layer"].nunique()
    )

# Présentation lisible des destinations étudiées, sans afficher directement une
# liste Python brute à l’écran.
destination_labels = sorted(
    df["destination"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

st.caption(
    "Destinations étudiées : " + ", ".join(destination_labels) + "."
)

# Encadré méthodologique : il rappelle les règles essentielles qui guident les
# visualisations et évitent des interprétations incorrectes.
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
        recettes touristiques et provenance des touristes. Les valeurs
        manquantes restent manquantes et ne sont jamais remplacées par zéro.
        Les comparaisons de provenance respectent le périmètre propre à chaque
        source afin de ne pas créer une comparabilité artificielle.
    </div>
    """,
    unsafe_allow_html=True,
)

# Les informations suivantes sont utiles pour le développement et le contrôle
# qualité, mais elles restent repliées par défaut dans la version de présentation.
with st.expander("Contrôle technique du dataset"):

    st.write("#### Répartition des observations")

    layer_labels = {
        "arrivals": "Arrivées",
        "receipts": "Recettes",
        "provenance": "Provenance",
    }

    layer_counts = (
        df["dataset_layer"]
        .value_counts()
        .rename_axis("Couche")
        .reset_index(name="Observations")
    )

    layer_counts["Couche"] = (
        layer_counts["Couche"]
        .replace(layer_labels)
    )

    st.dataframe(
        layer_counts,
        use_container_width=True,
        hide_index=True,
    )

    st.write("#### Aperçu du dataset maître")
    st.caption(
        "Aperçu technique des 20 premières lignes, conservé pour le contrôle "
        "des colonnes, unités et niveaux de granularité."
    )

    st.dataframe(
        df.head(20),
        use_container_width=True,
        hide_index=True,
    )

# ==============================================================================
# TABLEAU DE BORD
# ==============================================================================

st.markdown("---")
st.header("Tableau de bord")

tab_trends, tab_origin, tab_map = st.tabs(
    ["Tendances", "Provenance", "Carte"]
)


# ==============================================================================
# ONGLET 1 — TENDANCES
# ==============================================================================

with tab_trends:
    st.subheader("Évolution du tourisme international")
    st.caption(
        "Cet onglet permet de comparer l'évolution temporelle des arrivées et "
        "des recettes touristiques. Les filtres agissent uniquement sur les "
        "observations disponibles dans le dataset maître."
    )

    # --------------------------------------------------------------------------
    # Sélection de l'indicateur
    # --------------------------------------------------------------------------

    indicator_label = st.selectbox(
        "Indicateur",
        ["Arrivées touristiques internationales", "Recettes touristiques"],
        key="trend_indicator"
    )

    layer_map = {
        "Arrivées touristiques internationales": "arrivals",
        "Recettes touristiques": "receipts",
    }

    selected_layer = layer_map[indicator_label]

    trends_df = df[
        (df["dataset_layer"] == selected_layer) &
        (df["value"].notna())
    ].copy()

    # --------------------------------------------------------------------------
    # Période disponible
    # --------------------------------------------------------------------------

    year_min = int(trends_df["year"].min())
    year_max = int(trends_df["year"].max())

    year_range = st.slider(
        "Période",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
        step=1,
        key="trend_year_range"
    )

    # --------------------------------------------------------------------------
    # Sélection des destinations
    # --------------------------------------------------------------------------

    destinations = sorted(
        trends_df["destination"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_destinations = st.multiselect(
        "Destinations",
        options=destinations,
        default=destinations,
        key="trend_destinations"
    )

    # --------------------------------------------------------------------------
    # Filtrage
    # --------------------------------------------------------------------------

    filtered_trends = trends_df[
        (trends_df["year"] >= year_range[0]) &
        (trends_df["year"] <= year_range[1]) &
        (trends_df["destination"].isin(selected_destinations))
    ].copy()

    # --------------------------------------------------------------------------
    # Affichage
    # --------------------------------------------------------------------------

    if filtered_trends.empty:
        st.info("Aucune donnée disponible pour cette sélection.")

    else:
        st.write(
            f"**{len(filtered_trends)} observations disponibles** "
            f"entre {year_range[0]} et {year_range[1]}."
        )

        # ----------------------------------------------------------------------
        # Graphique d'évolution
        # ----------------------------------------------------------------------

        if selected_layer == "arrivals":
            y_title = "Arrivées touristiques internationales"
        else:
            y_title = "Recettes touristiques internationales"

        chart = (
            alt.Chart(filtered_trends)
            .mark_line(point=True)
            .encode(
                x=alt.X(
                    "year:O",
                    title="Année"
                ),
                y=alt.Y(
                    "value:Q",
                    title=y_title
                ),
                color=alt.Color(
                    "destination:N",
                    title="Destination"
                ),
                tooltip=[
                    alt.Tooltip(
                        "destination:N",
                        title="Destination"
                    ),
                    alt.Tooltip(
                        "year:O",
                        title="Année"
                    ),
                    alt.Tooltip(
                        "value:Q",
                        title="Valeur",
                        format=",.0f"
                    ),
                    alt.Tooltip(
                        "unit:N",
                        title="Unité"
                    ),
                ]
            )
            .properties(
                height=500
            )
        )

        st.altair_chart(
            chart,
            use_container_width=True
        )

        # ----------------------------------------------------------------------
        # Tableau des données affichées
        # ----------------------------------------------------------------------

        st.write("### Données affichées")

        st.dataframe(
            filtered_trends[
                ["destination", "year", "value", "unit"]
            ].sort_values(
                ["destination", "year"]
            ),
            use_container_width=True,
            hide_index=True,
        )
        
                # ----------------------------------------------------------------------
        # Téléchargement des données filtrées
        # ----------------------------------------------------------------------

        export_df = filtered_trends[
            ["destination", "year", "value", "unit"]
        ].sort_values(
            ["destination", "year"]
        )

        csv_bytes = export_df.to_csv(index=False).encode("utf-8")

        file_name = (
            f"tendances_{selected_layer}_"
            f"{year_range[0]}_{year_range[1]}.csv"
        )

        st.download_button(
            label="Télécharger les données en CSV",
            data=csv_bytes,
            file_name=file_name,
            mime="text/csv",
        )
# ==============================================================================
# ONGLET 2 — PROVENANCE
# ==============================================================================

with tab_origin:
    st.subheader("Provenance des touristes")

    st.caption(
        "Les données de provenance ne présentent pas le même niveau de couverture "
        "pour toutes les destinations. Les comparaisons sont donc réalisées "
        "dans le périmètre propre à chaque source."
    )

    # --------------------------------------------------------------------------
    # Données de provenance
    # --------------------------------------------------------------------------

    provenance_df = df[
        (df["dataset_layer"] == "provenance") &
        (df["value"].notna())
    ].copy()

    # --------------------------------------------------------------------------
    # Diagnostic de la structure des données de provenance
    # --------------------------------------------------------------------------

    with st.expander("Diagnostic des données de provenance"):

        st.write("### Granularités")
        st.write(
            sorted(
                provenance_df["granularity"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

        st.write("### Unités")
        st.write(
            sorted(
                provenance_df["unit"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

        st.write("### Périmètres de couverture")
        st.write(
            sorted(
                provenance_df["coverage_scope"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

        st.write("### Indicateurs de qualité")
        st.write(
            sorted(
                provenance_df["quality_flag"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

    # --------------------------------------------------------------------------
    # Sélection de la destination
    # --------------------------------------------------------------------------

    provenance_destinations = sorted(
        provenance_df["destination"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_origin_destination = st.selectbox(
        "Destination",
        options=provenance_destinations,
        key="origin_destination"
    )

    destination_df = provenance_df[
        provenance_df["destination"] == selected_origin_destination
    ].copy()

    # --------------------------------------------------------------------------
    # Sélection de l'année
    # --------------------------------------------------------------------------

    available_years = sorted(
        destination_df["year"]
        .dropna()
        .astype(int)
        .unique()
        .tolist(),
        reverse=True
    )

    selected_origin_year = st.selectbox(
        "Année",
        options=available_years,
        key="origin_year"
    )

    origin_filtered = destination_df[
        destination_df["year"] == selected_origin_year
    ].copy()
    
    # --------------------------------------------------------------------------
    # Informations générales sur la sélection
    # --------------------------------------------------------------------------

    units = origin_filtered["unit"].dropna().unique().tolist()

    st.write(
        f"**{len(origin_filtered)} observations disponibles** "
        f"pour {selected_origin_destination} en {selected_origin_year}."
    )

    st.write(
        "**Unité disponible :** "
        + ", ".join(units)
    )

    # --------------------------------------------------------------------------
    # Marchés d'origine de granularité COUNTRY
    # --------------------------------------------------------------------------

    country_origins = origin_filtered[
        origin_filtered["granularity"] == "country"
    ].copy()

    if country_origins.empty:

        st.warning(
            "Aucune donnée par pays d'origine n'est disponible "
            "pour cette sélection."
        )

    else:

        origin_units = (
            country_origins["unit"]
            .dropna()
            .unique()
            .tolist()
        )

        if len(origin_units) > 1:

            st.warning(
                "Plusieurs unités sont présentes dans cette sélection. "
                "Les données ne sont pas combinées."
            )

        else:

            origin_unit = origin_units[0]

            # ------------------------------------------------------------------
            # Libellé et format de l'unité
            # ------------------------------------------------------------------
            # ------------------------------------------------------------------
            # Préparation de la valeur affichée
            # ------------------------------------------------------------------

            country_origins = country_origins.copy()

            if origin_unit == "persons":
                value_title = "Touristes"
                tooltip_format = ",.0f"

                country_origins["display_value"] = country_origins["value"]

            elif origin_unit == "share":
                value_title = "Part des touristes (%)"
                tooltip_format = ".1f"

                # Les parts sont stockées sous forme décimale :
                # 0.15 = 15 %
                # On multiplie uniquement pour l'affichage.
                country_origins["display_value"] = (
                    country_origins["value"] * 100
                )

            else:
                value_title = origin_unit
                tooltip_format = ",.2f"

                country_origins["display_value"] = country_origins["value"]

            # ------------------------------------------------------------------
            # Classement des marchés
            # ------------------------------------------------------------------

            country_origins = country_origins.sort_values(
                "display_value",
                ascending=False
            )

            # ------------------------------------------------------------------
            # Classement des marchés
            # ------------------------------------------------------------------

            # ------------------------------------------------------------------
            # Graphique
            # ------------------------------------------------------------------

            origin_chart = (
                alt.Chart(country_origins)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "display_value:Q",
                        title=value_title,
                    ),
                    y=alt.Y(
                        "origin_name:N",
                        title="Marché d'origine",
                        sort="-x"
                    ),
                    tooltip=[
                        alt.Tooltip(
                            "origin_name:N",
                            title="Marché d'origine"
                        ),
                        alt.Tooltip(
                            "display_value:Q",
                            title=value_title,
                            format=tooltip_format
                        ),
                        alt.Tooltip(
                            "quality_flag:N",
                            title="Qualité / périmètre"
                        ),
                        alt.Tooltip(
                            "coverage_scope:N",
                            title="Couverture"
                        ),
                    ]
                )
                .properties(
                    height=max(
                        350,
                        len(country_origins) * 28
                    )
                )
            )

            st.write(
                f"### Marchés d'origine — "
                f"{selected_origin_destination} — "
                f"{selected_origin_year}"
            )

            st.altair_chart(
                origin_chart,
                use_container_width=True
            )

            st.caption(
                "Le graphique présente uniquement les observations "
                "de granularité « country ». Les agrégats régionaux, "
                "totaux et données de diaspora sont exclus."
            )

    # --------------------------------------------------------------------------
    # Cas particulier : Égypte
    # --------------------------------------------------------------------------
    # L’Égypte dispose d’une couverture pays incomplète. On sépare donc
    # explicitement le marché-pays vérifié des parts régionales de 2019.

    if selected_origin_destination == "Égypte":

        st.markdown("---")
        st.subheader("Données disponibles pour l'Égypte")

        st.markdown(
    f"""
    <div style="
        background-color: {CORP['panel']};
        color: {CORP['text']};
        border-left: 5px solid {CORP['accent']};
        padding: 14px 16px;
        border-radius: 8px;
        margin: 10px 0 20px 0;
        font-size: 0.95rem;
        line-height: 1.5;
    ">
        <strong>Comparabilité limitée — Égypte</strong><br>
        La couverture par pays est incomplète. Les États-Unis constituent
        le seul marché-pays vérifié dans le dataset et ne doivent donc pas
        être interprétés comme le principal marché d'origine de l'Égypte.
    </div>
    """,
    unsafe_allow_html=True,
)

        # ----------------------------------------------------------------------
        # 1. Marché-pays vérifié
        # ----------------------------------------------------------------------

        egypt_country = origin_filtered[
            (origin_filtered["granularity"] == "country") &
            (origin_filtered["unit"] == "persons")
        ].copy()

        if not egypt_country.empty:

            st.write(
                f"### Marché-pays vérifié — {selected_origin_year}"
            )

            egypt_country_chart = (
                alt.Chart(egypt_country)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "value:Q",
                        title="Touristes"
                    ),
                    y=alt.Y(
                        "origin_name:N",
                        title="Marché d'origine"
                    ),
                    tooltip=[
                        alt.Tooltip(
                            "origin_name:N",
                            title="Marché"
                        ),
                        alt.Tooltip(
                            "value:Q",
                            title="Touristes",
                            format=",.0f"
                        ),
                        alt.Tooltip(
                            "coverage_scope:N",
                            title="Couverture"
                        ),
                    ]
                )
                .properties(
                    height=180
                )
            )

            st.altair_chart(
                egypt_country_chart,
                use_container_width=True
            )

        # ----------------------------------------------------------------------
        # 2. Répartition régionale
        # ----------------------------------------------------------------------

        egypt_regions = provenance_df[
    (provenance_df["destination"] == "Égypte") &
    (provenance_df["year"] == 2019) &
    (provenance_df["granularity"] == "regional_aggregate") &
    (provenance_df["unit"] == "share") &
    (provenance_df["metric_type"] == "regional_tourist_share") &
    (provenance_df["value"].notna())
].copy()

        if not egypt_regions.empty:

            egypt_regions["display_value"] = (
                egypt_regions["value"] * 100
            )

            egypt_regions = egypt_regions.sort_values(
                "display_value",
                ascending=False
            )

            st.write("### Répartition régionale — 2019")

            st.caption(
                "Les données régionales sont exprimées en parts (%) et sont "
                "présentées séparément des volumes par pays."
            )

            egypt_region_chart = (
                alt.Chart(egypt_regions)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "display_value:Q",
                        title="Part des touristes (%)"
                    ),
                    y=alt.Y(
                        "origin_name:N",
                        title="Région d'origine",
                        sort="-x"
                    ),
                    tooltip=[
                        alt.Tooltip(
                            "origin_name:N",
                            title="Région"
                        ),
                        alt.Tooltip(
                            "display_value:Q",
                            title="Part des touristes (%)",
                            format=".1f"
                        ),
                    ]
                )
                .properties(
                    height=300
                )
            )

            st.altair_chart(
                egypt_region_chart,
                use_container_width=True
            )
    # --------------------------------------------------------------------------
    # Tableau complet de contrôle
    # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
    # Tableau des données de provenance
    # --------------------------------------------------------------------------

    st.write("### Données de provenance disponibles")

    origin_display = origin_filtered[
        [
            "origin_name",
            "origin_region",
            "granularity",
            "value",
            "unit",
            "coverage_scope",
            "quality_flag",
        ]
    ].copy()

    # --------------------------------------------------------------------------
    # Valeur lisible pour l'affichage
    # --------------------------------------------------------------------------

    origin_display["Valeur affichée"] = origin_display.apply(
        lambda row:
            f"{row['value'] * 100:.1f} %"
            if row["unit"] == "share"
            else f"{row['value']:,.0f}"
            if row["unit"] == "persons"
            else str(row["value"]),
        axis=1
    )

    # Trier selon la vraie valeur numérique
    origin_display = origin_display.sort_values(
        "value",
        ascending=False
    )

    # --------------------------------------------------------------------------
    # Renommage des colonnes pour le dashboard
    # --------------------------------------------------------------------------

    origin_display = origin_display.rename(
        columns={
            "origin_name": "Marché d'origine",
            "origin_region": "Région d'origine",
            "granularity": "Granularité",
            "unit": "Unité",
            "coverage_scope": "Périmètre",
            "quality_flag": "Qualité",
        }
    )

    # La valeur brute reste dans le dataset mais n'est pas affichée ici
    origin_display = origin_display[
        [
            "Marché d'origine",
            "Région d'origine",
            "Granularité",
            "Valeur affichée",
            "Unité",
            "Périmètre",
            "Qualité",
        ]
    ]

    st.dataframe(
        origin_display,
        use_container_width=True,
        hide_index=True,
    )
        # --------------------------------------------------------------------------
    # Téléchargement des données de provenance sélectionnées
    # --------------------------------------------------------------------------

    export_origin = origin_filtered[
        [
            "destination",
            "year",
            "origin_name",
            "origin_region",
            "granularity",
            "value",
            "unit",
            "coverage_scope",
            "quality_flag",
        ]
    ].copy()

    export_origin = export_origin.sort_values(
        ["granularity", "value"],
        ascending=[True, False]
    )

    origin_csv = export_origin.to_csv(
        index=False
    ).encode("utf-8")

    origin_file_name = (
        f"provenance_"
        f"{selected_origin_destination}_"
        f"{selected_origin_year}.csv"
    )

    st.download_button(
        label="Télécharger les données de provenance en CSV",
        data=origin_csv,
        file_name=origin_file_name,
        mime="text/csv",
        key="download_origin"
    )
# ==============================================================================
# ONGLET 3 — CARTE
# ==============================================================================

with tab_map:
    st.subheader("Comparaison géographique")

    st.caption(
        "Version exploratoire : la carte compare les niveaux d'arrivées ou de "
        "recettes touristiques pour une année donnée. Les valeurs manquantes "
        "restent non renseignées et ne sont pas remplacées par zéro."
    )

    # --------------------------------------------------------------------------
    # Vérification Plotly
    # --------------------------------------------------------------------------

    if not HAS_PLOTLY:
        st.error(
            "Plotly n'est pas installé. Installez-le avec : "
            "py -m pip install plotly"
        )
        st.stop()

    # --------------------------------------------------------------------------
    # Sélection de l'indicateur
    # --------------------------------------------------------------------------

    map_indicator_label = st.selectbox(
        "Indicateur cartographié",
        [
            "Arrivées touristiques internationales",
            "Recettes touristiques"
        ],
        key="map_indicator"
    )

    map_layer_map = {
        "Arrivées touristiques internationales": "arrivals",
        "Recettes touristiques": "receipts",
    }

    map_layer = map_layer_map[map_indicator_label]

    map_source = df[
        (df["dataset_layer"] == map_layer) &
        (df["value"].notna())
    ].copy()

    # --------------------------------------------------------------------------
    # Sélection de l'année
    # --------------------------------------------------------------------------

    map_years = sorted(
        map_source["year"]
        .dropna()
        .astype(int)
        .unique()
        .tolist(),
        reverse=True
    )

    map_year = st.selectbox(
        "Année",
        options=map_years,
        key="map_year"
    )

    # --------------------------------------------------------------------------
    # Données de l'année sélectionnée
    # --------------------------------------------------------------------------

    map_df = map_source[
        map_source["year"] == map_year
    ][
        [
            "destination",
            "value",
            "unit"
        ]
    ].copy()

    # --------------------------------------------------------------------------
    # Noms de pays compatibles avec Plotly
    # --------------------------------------------------------------------------

    country_name_map = {
        "Maroc": "Morocco",
        "Afrique du Sud": "South Africa",
        "Égypte": "Egypt",
        "Tunisie": "Tunisia",
        "Kenya": "Kenya",
        "Tanzanie": "Tanzania",
        "Maurice": "Mauritius",
    }

    map_df["country_plotly"] = (
        map_df["destination"]
        .replace(country_name_map)
    )

    # --------------------------------------------------------------------------
    # Libellé
    # --------------------------------------------------------------------------

    if map_layer == "arrivals":
        map_value_label = "Arrivées touristiques"
    else:
        map_value_label = "Recettes touristiques"

    # --------------------------------------------------------------------------
    # Carte
    # --------------------------------------------------------------------------

    fig = px.choropleth(
        map_df,
        locations="country_plotly",
        locationmode="country names",
        color="value",
        scope="africa",
        hover_name="destination",
        hover_data={
            "value": ":,.0f",
            "unit": True,
            "country_plotly": False,
        },
        labels={
            "value": map_value_label,
            "unit": "Unité",
        },
        title=f"{map_value_label} — Afrique — {map_year}",
    )

    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        ),
        paper_bgcolor=CORP["bg"],
        font_color=CORP["text"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------------------------
    # Données cartographiées
    # --------------------------------------------------------------------------

    st.write("### Données cartographiées")

    map_display = map_df[
        [
            "destination",
            "value",
            "unit"
        ]
    ].sort_values(
        "value",
        ascending=False
    )

    st.dataframe(
        map_display,
        use_container_width=True,
        hide_index=True
    )
