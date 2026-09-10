import pandas as pd


def filter_layer(df: pd.DataFrame, layer: str) -> pd.DataFrame:
    """
    Filtre le dataset maître sur une couche donnée :
    arrivals, receipts ou provenance.
    """
    return df[df["dataset_layer"] == layer].copy()


def get_available_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Conserve uniquement les observations disposant d'une valeur.
    Les valeurs manquantes ne sont jamais remplacées par zéro.
    """
    return df[df["value"].notna()].copy()


def get_latest_year_by_destination(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retourne la dernière année disposant d'une valeur
    pour chaque destination.
    """
    available = get_available_values(df)

    return (
        available.groupby("destination", as_index=False)["year"]
        .max()
        .rename(columns={"year": "derniere_annee_disponible"})
    )


def get_latest_value_by_destination(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retourne la valeur correspondant à la dernière année disponible
    pour chaque destination.
    """
    available = get_available_values(df)

    latest_idx = (
        available.groupby("destination")["year"]
        .idxmax()
    )

    return (
        available.loc[
            latest_idx,
            ["destination", "year", "value"]
        ]
        .sort_values("value", ascending=False)
        .reset_index(drop=True)
    )