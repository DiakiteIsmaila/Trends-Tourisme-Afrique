from pathlib import Path
import pandas as pd


def load_master_dataset(data_path: Path) -> pd.DataFrame:
    """
    Charge le dataset maître Trends depuis un fichier CSV.
    """
    return pd.read_csv(data_path)


def get_dataset_overview(df: pd.DataFrame) -> dict:
    """
    Retourne les informations générales du dataset.
    """
    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isna().sum().to_dict(),
        "destinations": df["destination"].dropna().unique().tolist(),
        "dataset_layers": df["dataset_layer"].value_counts().to_dict(),
    }


def get_observations_by_destination(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compte les observations par destination et par couche de données.
    """
    return pd.crosstab(
        df["destination"],
        df["dataset_layer"]
    )


def get_value_quality_by_layer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compte les observations, valeurs disponibles et valeurs manquantes
    pour chaque couche du dataset.
    """
    return (
        df.groupby("dataset_layer")["value"]
        .agg(
            observations="size",
            valeurs_disponibles="count",
            valeurs_manquantes=lambda x: x.isna().sum()
        )
    )


def get_temporal_coverage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule la période couverte par destination et par couche de données.
    """
    return (
        df.groupby(["destination", "dataset_layer"])
        .agg(
            annee_debut=("year", "min"),
            annee_fin=("year", "max"),
            observations=("year", "size")
        )
        .reset_index()
    )