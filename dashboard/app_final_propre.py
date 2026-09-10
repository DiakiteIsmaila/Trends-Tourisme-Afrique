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
        /* Fond général de l'application */
        .stApp {{
            background-color: {CORP["bg"]};
            color: {CORP["text"]};
        }}

        /* Conteneur principal : largeur confortable pour les graphiques */
        .block-container {{
            background: transparent;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}

        /* Texte courant */
        .stApp p,
        .stApp label,
        .stApp li {{
            color: {CORP["text"]};
        }}

        /* Contraste des KPI */
        [data-testid="stMetricLabel"] p,
        [data-testid="stMetricLabel"] div,
        [data-testid="stMetricValue"] div {{
            color: {CORP["text"]} !important;
        }}

        /* Onglets */
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

        /* Boutons de téléchargement */
        .stDownloadButton button {{
            border-color: {CORP["accent"]};
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
        use_container_width=True,
        hide_index=True,
    )

    st.write("#### Aperçu du dataset maître")
    st.caption(
        "Les 20 premières lignes sont conservées ici pour contrôler les colonnes, "
        "les unités et les niveaux de granularité."
    )

    st.dataframe(
        df.head(20),
        use_container_width=True,
        hide_index=True,
    )


# ==============================================================================
# 6. TABLEAU DE BORD — NAVIGATION PRINCIPALE
# ==============================================================================

st.markdown("---")
st.header("Tableau de bord")

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
    st.subheader("Évolution du tourisme international")

    st.caption(
        "Cet onglet permet d'analyser l'évolution temporelle des arrivées et "
        "des recettes touristiques internationales pour les sept destinations. "
        "Les filtres permettent de comparer plusieurs pays sur une même période "
        "ou d'examiner individuellement leur trajectoire."
    )

    # --------------------------------------------------------------------------
    # 1. Choix de l'indicateur
    # --------------------------------------------------------------------------
    indicator_label = st.selectbox(
        "Indicateur",
        [
            "Arrivées touristiques internationales",
            "Recettes touristiques",
        ],
        key="trend_indicator",
    )

    layer_map = {
        "Arrivées touristiques internationales": "arrivals",
        "Recettes touristiques": "receipts",
    }

    selected_layer = layer_map[indicator_label]

    # On conserve uniquement les observations réellement disponibles.
    trends_df = df[
        (df["dataset_layer"] == selected_layer)
        & (df["value"].notna())
    ].copy()

    # --------------------------------------------------------------------------
    # 2. Choix de la période
    # --------------------------------------------------------------------------
    year_min = int(trends_df["year"].min())
    year_max = int(trends_df["year"].max())

    year_range = st.slider(
        "Période",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
        step=1,
        key="trend_year_range",
    )

    # --------------------------------------------------------------------------
    # 3. Choix des destinations
    # --------------------------------------------------------------------------
    destinations = ordered_destinations(trends_df["destination"])

    selected_destinations = st.multiselect(
        "Destinations",
        options=destinations,
        default=destinations,
        key="trend_destinations",
    )

    # --------------------------------------------------------------------------
    # 4. Filtrage
    # --------------------------------------------------------------------------
    filtered_trends = trends_df[
        (trends_df["year"] >= year_range[0])
        & (trends_df["year"] <= year_range[1])
        & (trends_df["destination"].isin(selected_destinations))
    ].copy()

    if filtered_trends.empty:
        st.info("Aucune donnée disponible pour cette sélection.")

    else:
        st.write(
            f"**{len(filtered_trends)} observations disponibles** "
            f"entre {year_range[0]} et {year_range[1]}."
        )

        # ----------------------------------------------------------------------
        # 5. Graphique d'évolution
        # ----------------------------------------------------------------------
        if selected_layer == "arrivals":
            y_title = "Arrivées touristiques internationales"
        else:
            y_title = "Recettes touristiques"

        chart = (
            alt.Chart(filtered_trends)
            .mark_line(point=True)
            .encode(
                x=alt.X(
                    "year:O",
                    title="Année",
                ),
                y=alt.Y(
                    "value:Q",
                    title=y_title,
                ),
                color=alt.Color(
                    "destination:N",
                    title="Destination",
                ),
                tooltip=[
                    alt.Tooltip(
                        "destination:N",
                        title="Destination",
                    ),
                    alt.Tooltip(
                        "year:O",
                        title="Année",
                    ),
                    alt.Tooltip(
                        "value:Q",
                        title="Valeur",
                        format=",.0f",
                    ),
                    alt.Tooltip(
                        "unit:N",
                        title="Unité",
                    ),
                ],
            )
            .properties(height=500)
        )

        st.altair_chart(
            chart,
            use_container_width=True,
        )

        st.caption(
            "Lecture : chaque courbe représente une destination. Une interruption "
            "ou une absence de point correspond à une donnée non disponible ; elle "
            "n'est pas interprétée comme une valeur nulle."
        )

        # ----------------------------------------------------------------------
        # 6. Tableau des observations affichées
        # ----------------------------------------------------------------------
        st.write("### Données affichées")

        trends_display = (
            filtered_trends[
                ["destination", "year", "value", "unit"]
            ]
            .sort_values(["destination", "year"])
            .rename(
                columns={
                    "destination": "Destination",
                    "year": "Année",
                    "value": "Valeur",
                    "unit": "Unité",
                }
            )
        )

        st.dataframe(
            trends_display,
            use_container_width=True,
            hide_index=True,
        )

        # ----------------------------------------------------------------------
        # 7. Export CSV
        # ----------------------------------------------------------------------
        # L'export conserve les valeurs numériques brutes du dataset.
        export_df = filtered_trends[
            ["destination", "year", "value", "unit"]
        ].sort_values(["destination", "year"])

        csv_bytes = export_df.to_csv(index=False).encode("utf-8")

        file_name = (
            f"tendances_{selected_layer}_"
            f"{year_range[0]}_{year_range[1]}.csv"
        )

        st.download_button(
            label="Télécharger les données affichées en CSV",
            data=csv_bytes,
            file_name=file_name,
            mime="text/csv",
            key="download_trends",
        )


# ==============================================================================
# ONGLET 2 — PROVENANCE
# ==============================================================================
# Objectif :
# montrer les marchés d'origine disponibles sans forcer une comparaison entre
# des sources qui n'ont pas le même périmètre, la même granularité ou la même
# unité de mesure.

with tab_origin:
    st.subheader("Provenance des touristes")

    st.caption(
        "Cet onglet analyse l'origine géographique des touristes selon les données "
        "disponibles pour chaque destination. La couverture varie selon les sources : "
        "les comparaisons sont donc limitées aux périmètres réellement disponibles "
        "et aucun marché manquant n'est reconstitué."
    )

    # --------------------------------------------------------------------------
    # 1. Préparation des données de provenance
    # --------------------------------------------------------------------------
    provenance_df = df[
        (df["dataset_layer"] == "provenance")
        & (df["value"].notna())
    ].copy()

    # Diagnostic technique disponible à la demande.
    with st.expander("Diagnostic des données de provenance"):
        diagnostic_col1, diagnostic_col2 = st.columns(2)

        with diagnostic_col1:
            st.write("#### Granularités")
            st.write(
                sorted(
                    provenance_df["granularity"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )

            st.write("#### Unités")
            st.write(
                sorted(
                    provenance_df["unit"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )

        with diagnostic_col2:
            st.write("#### Périmètres de couverture")
            st.write(
                sorted(
                    provenance_df["coverage_scope"]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )

            st.write("#### Indicateurs de qualité")
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
    # 2. Sélection de la destination et de l'année
    # --------------------------------------------------------------------------
    provenance_destinations = ordered_destinations(
        provenance_df["destination"]
    )

    selected_origin_destination = st.selectbox(
        "Destination",
        options=provenance_destinations,
        key="origin_destination",
    )

    destination_df = provenance_df[
        provenance_df["destination"] == selected_origin_destination
    ].copy()

    available_years = sorted(
        destination_df["year"]
        .dropna()
        .astype(int)
        .unique()
        .tolist(),
        reverse=True,
    )

    selected_origin_year = st.selectbox(
        "Année",
        options=available_years,
        key="origin_year",
    )

    origin_filtered = destination_df[
        destination_df["year"] == selected_origin_year
    ].copy()

    units = sorted(
        origin_filtered["unit"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    st.write(
        f"**{len(origin_filtered)} observations disponibles** "
        f"pour {selected_origin_destination} en {selected_origin_year}."
    )

    if units:
        st.caption("Unité(s) présente(s) dans la sélection : " + ", ".join(units))

    # --------------------------------------------------------------------------
    # 3. Visualisation
    # --------------------------------------------------------------------------
    # Égypte : cas traité séparément car le dataset ne contient qu'un marché-pays
    # vérifié (États-Unis), complété par une répartition régionale pour 2019.
    if selected_origin_destination == "Égypte":

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
                La répartition régionale de 2019 est présentée séparément.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------------------------
        # 3A. Marché-pays vérifié
        # ----------------------------------------------------------------------
        egypt_country = origin_filtered[
            (origin_filtered["granularity"] == "country")
            & (origin_filtered["unit"] == "persons")
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
                        title="Touristes",
                    ),
                    y=alt.Y(
                        "origin_name:N",
                        title="Marché d'origine",
                    ),
                    tooltip=[
                        alt.Tooltip(
                            "origin_name:N",
                            title="Marché",
                        ),
                        alt.Tooltip(
                            "value:Q",
                            title="Touristes",
                            format=",.0f",
                        ),
                        alt.Tooltip(
                            "coverage_scope:N",
                            title="Couverture",
                        ),
                    ],
                )
                .properties(height=180)
            )

            st.altair_chart(
                egypt_country_chart,
                use_container_width=True,
            )

            st.caption(
                "Cette barre indique uniquement le marché-pays vérifié disponible "
                "dans la source. Elle ne constitue pas un classement complet des "
                "marchés émetteurs de l'Égypte."
            )

        # ----------------------------------------------------------------------
        # 3B. Répartition régionale des touristes — 2019
        # ----------------------------------------------------------------------
        # Ce filtre utilise explicitement regional_tourist_share afin de ne pas
        # mélanger la part des touristes et la part des nuitées.
        egypt_regions = provenance_df[
            (provenance_df["destination"] == "Égypte")
            & (provenance_df["year"] == 2019)
            & (provenance_df["granularity"] == "regional_aggregate")
            & (provenance_df["unit"] == "share")
            & (provenance_df["metric_type"] == "regional_tourist_share")
            & (provenance_df["value"].notna())
        ].copy()

        if not egypt_regions.empty:
            egypt_regions["display_value"] = egypt_regions["value"] * 100
            egypt_regions = egypt_regions.sort_values(
                "display_value",
                ascending=False,
            )

            st.markdown("---")
            st.write("### Répartition régionale des touristes — 2019")

            st.caption(
                "Ces données représentent des parts régionales de touristes en 2019. "
                "Elles sont distinctes des volumes par pays et des parts de nuitées."
            )

            egypt_region_chart = (
                alt.Chart(egypt_regions)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "display_value:Q",
                        title="Part des touristes (%)",
                    ),
                    y=alt.Y(
                        "origin_name:N",
                        title="Région d'origine",
                        sort="-x",
                    ),
                    tooltip=[
                        alt.Tooltip(
                            "origin_name:N",
                            title="Région",
                        ),
                        alt.Tooltip(
                            "display_value:Q",
                            title="Part des touristes (%)",
                            format=".1f",
                        ),
                    ],
                )
                .properties(height=300)
            )

            st.altair_chart(
                egypt_region_chart,
                use_container_width=True,
            )

    else:
        # ----------------------------------------------------------------------
        # 3C. Cas général : observations de granularité « country »
        # ----------------------------------------------------------------------
        # Les agrégats régionaux, totaux et données de diaspora restent visibles
        # dans le tableau de contrôle, mais ne sont pas mélangés au graphique.
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
                .astype(str)
                .unique()
                .tolist()
            )

            if len(origin_units) > 1:
                st.warning(
                    "Plusieurs unités sont présentes dans cette sélection. "
                    "Elles ne sont pas combinées dans un même graphique."
                )

            else:
                origin_unit = origin_units[0]
                country_origins = country_origins.copy()

                if origin_unit == "persons":
                    value_title = "Touristes"
                    tooltip_format = ",.0f"
                    country_origins["display_value"] = country_origins["value"]

                elif origin_unit == "share":
                    value_title = "Part des touristes (%)"
                    tooltip_format = ".1f"

                    # Les parts sont stockées sous forme décimale : 0.15 = 15 %.
                    country_origins["display_value"] = (
                        country_origins["value"] * 100
                    )

                else:
                    value_title = origin_unit
                    tooltip_format = ",.2f"
                    country_origins["display_value"] = country_origins["value"]

                country_origins = country_origins.sort_values(
                    "display_value",
                    ascending=False,
                )

                st.write(
                    f"### Marchés d'origine — "
                    f"{selected_origin_destination} — "
                    f"{selected_origin_year}"
                )

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
                            sort="-x",
                        ),
                        tooltip=[
                            alt.Tooltip(
                                "origin_name:N",
                                title="Marché d'origine",
                            ),
                            alt.Tooltip(
                                "display_value:Q",
                                title=value_title,
                                format=tooltip_format,
                            ),
                            alt.Tooltip(
                                "quality_flag:N",
                                title="Qualité / périmètre",
                            ),
                            alt.Tooltip(
                                "coverage_scope:N",
                                title="Couverture",
                            ),
                        ],
                    )
                    .properties(
                        height=max(350, len(country_origins) * 28)
                    )
                )

                st.altair_chart(
                    origin_chart,
                    use_container_width=True,
                )

                st.caption(
                    "Le graphique présente uniquement les observations de granularité "
                    "« country ». Les agrégats régionaux, totaux et données de diaspora "
                    "sont volontairement exclus pour éviter de mélanger des niveaux "
                    "d'analyse différents."
                )

    # --------------------------------------------------------------------------
    # 4. Tableau complet de la sélection
    # --------------------------------------------------------------------------
    st.write("### Données de provenance disponibles")

    # metric_type est conservé dans le tableau afin de distinguer, notamment
    # pour l'Égypte, la part des touristes de la part des nuitées.
    origin_display = origin_filtered[
        [
            "origin_name",
            "origin_region",
            "granularity",
            "metric_type",
            "value",
            "unit",
            "coverage_scope",
            "quality_flag",
        ]
    ].copy()

    origin_display["Valeur affichée"] = origin_display.apply(
        lambda row: format_display_value(row["value"], row["unit"]),
        axis=1,
    )

    origin_display["Type d'indicateur"] = (
        origin_display["metric_type"]
        .replace(METRIC_TYPE_LABELS)
    )

    origin_display = origin_display.sort_values(
        "value",
        ascending=False,
    )

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

    origin_display = origin_display[
        [
            "Marché d'origine",
            "Région d'origine",
            "Granularité",
            "Type d'indicateur",
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
    # 5. Export CSV
    # --------------------------------------------------------------------------
    # L'export conserve les valeurs brutes : une part de 15 % reste 0.15 avec
    # unit == "share". Cela préserve l'intégrité analytique du dataset.
    export_origin_columns = [
        "destination",
        "year",
        "origin_name",
        "origin_region",
        "granularity",
        "metric_type",
        "value",
        "unit",
        "coverage_scope",
        "quality_flag",
    ]

    export_origin = (
        origin_filtered[export_origin_columns]
        .sort_values(["granularity", "value"], ascending=[True, False])
    )

    origin_csv = export_origin.to_csv(index=False).encode("utf-8")

    origin_file_name = (
        f"provenance_"
        f"{safe_filename(selected_origin_destination)}_"
        f"{selected_origin_year}.csv"
    )

    st.download_button(
        label="Télécharger les données de provenance en CSV",
        data=origin_csv,
        file_name=origin_file_name,
        mime="text/csv",
        key="download_origin",
    )


# ==============================================================================
# ONGLET 3 — CARTE
# ==============================================================================
# Objectif :
# fournir une lecture géographique des arrivées ou des recettes pour une année
# donnée. Les codes ISO-3 sont utilisés pour fiabiliser la reconnaissance des
# sept destinations, notamment Maurice (MUS).

with tab_map:
    st.subheader("Comparaison géographique")

    st.caption(
        "Cet onglet propose une lecture géographique des arrivées ou des recettes "
        "touristiques pour une année donnée. Les pays sans observation disponible "
        "restent sans valeur : aucune donnée manquante n'est transformée en zéro."
    )

    if not HAS_PLOTLY:
        st.error(
            "Plotly n'est pas installé. Installez-le avec : "
            "py -m pip install plotly"
        )

    else:
        # ----------------------------------------------------------------------
        # 1. Choix de l'indicateur
        # ----------------------------------------------------------------------
        map_indicator_label = st.selectbox(
            "Indicateur cartographié",
            [
                "Arrivées touristiques internationales",
                "Recettes touristiques",
            ],
            key="map_indicator",
        )

        map_layer_map = {
            "Arrivées touristiques internationales": "arrivals",
            "Recettes touristiques": "receipts",
        }

        map_layer = map_layer_map[map_indicator_label]

        map_source = df[
            (df["dataset_layer"] == map_layer)
            & (df["value"].notna())
        ].copy()

        # ----------------------------------------------------------------------
        # 2. Choix de l'année
        # ----------------------------------------------------------------------
        map_years = sorted(
            map_source["year"]
            .dropna()
            .astype(int)
            .unique()
            .tolist(),
            reverse=True,
        )

        map_year = st.selectbox(
            "Année",
            options=map_years,
            key="map_year",
        )

        # ----------------------------------------------------------------------
        # 3. Données réellement disponibles pour l'année
        # ----------------------------------------------------------------------
        map_df = map_source[
            map_source["year"] == map_year
        ][
            ["destination", "value", "unit"]
        ].copy()

        map_df["iso_alpha"] = map_df["destination"].map(COUNTRY_ISO_MAP)

        # Le diagnostic ci-dessous détecte immédiatement un nom de pays qui
        # n'aurait pas de code ISO associé.
        unmapped = map_df[
            map_df["iso_alpha"].isna()
        ]["destination"].dropna().unique().tolist()

        if unmapped:
            st.warning(
                "Certaines destinations ne peuvent pas être cartographiées : "
                + ", ".join(unmapped)
            )

        mapped_df = map_df[
            map_df["iso_alpha"].notna()
        ].copy()

        if map_layer == "arrivals":
            map_value_label = "Arrivées touristiques"
        else:
            map_value_label = "Recettes touristiques"

        # ----------------------------------------------------------------------
        # 4. Information de couverture
        # ----------------------------------------------------------------------
        available_map_destinations = set(mapped_df["destination"].tolist())
        all_project_destinations = set(
            ordered_destinations(df["destination"])
        )
        missing_map_destinations = [
            d
            for d in DESTINATION_ORDER
            if d in all_project_destinations
            and d not in available_map_destinations
        ]

        st.write(
            f"**{len(available_map_destinations)} destination(s) cartographiée(s)** "
            f"pour {map_year}."
        )

        if missing_map_destinations:
            st.caption(
                "Sans valeur disponible pour cette année : "
                + ", ".join(missing_map_destinations)
                + "."
            )

        # ----------------------------------------------------------------------
        # 5. Carte choroplèthe
        # ----------------------------------------------------------------------
        if mapped_df.empty:
            st.info("Aucune donnée cartographiable pour cette sélection.")

        else:
            fig = px.choropleth(
                mapped_df,
                locations="iso_alpha",
                locationmode="ISO-3",
                color="value",
                scope="africa",
                hover_name="destination",
                hover_data={
                    "value": ":,.0f",
                    "unit": True,
                    "iso_alpha": False,
                },
                labels={
                    "value": map_value_label,
                    "unit": "Unité",
                },
                title=f"{map_value_label} — Afrique — {map_year}",
                color_continuous_scale=[
                    CORP["panel"],
                    CORP["accent"],
                ],
            )

            fig.update_layout(
                margin=dict(l=10, r=10, t=60, b=10),
                paper_bgcolor=CORP["bg"],
                font_color=CORP["text"],
            )

            fig.update_geos(
                bgcolor=CORP["bg"],
                showcoastlines=True,
                showland=True,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

            st.caption(
                "La couleur traduit uniquement les valeurs effectivement présentes "
                "dans le dataset pour l'année sélectionnée. Un pays non renseigné "
                "n'est pas interprété comme ayant une valeur égale à zéro."
            )

        # ----------------------------------------------------------------------
        # 6. Tableau des données cartographiées
        # ----------------------------------------------------------------------
        st.write("### Données cartographiées")

        map_display = (
            map_df[
                ["destination", "value", "unit"]
            ]
            .sort_values("value", ascending=False)
            .rename(
                columns={
                    "destination": "Destination",
                    "value": "Valeur",
                    "unit": "Unité",
                }
            )
        )

        st.dataframe(
            map_display,
            use_container_width=True,
            hide_index=True,
        )

        # ----------------------------------------------------------------------
        # 7. Export CSV
        # ----------------------------------------------------------------------
        map_export = map_df[
            ["destination", "value", "unit"]
        ].sort_values("value", ascending=False)

        map_csv = map_export.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Télécharger les données cartographiées en CSV",
            data=map_csv,
            file_name=f"carte_{map_layer}_{map_year}.csv",
            mime="text/csv",
            key="download_map",
        )
