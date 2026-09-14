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
def national_series(df, indicator):
    """National values or strict annual receipts/arrivals pairs; never impute."""
    keys = ["destination", "year"]
    tables = {}
    for layer, unit in [("arrivals", "persons"), ("receipts", "current_USD")]:
        table = df.loc[df.dataset_layer.eq(layer)].copy()
        if table.duplicated(keys).any():
            raise ValueError("Duplicate national destination/year")
        if not table.unit.eq(unit).all() or not table.granularity.eq("destination_total").all():
            raise ValueError("Invalid national units or granularity")
        tables[layer] = table
    if indicator in tables:
        return tables[indicator]
    if indicator != "ratio":
        raise ValueError("Unknown indicator")
    result = tables["arrivals"][keys + ["value"]].rename(columns={"value": "arrivals"}).merge(
        tables["receipts"][keys + ["value"]].rename(columns={"value": "receipts"}),
        on=keys, how="outer", validate="one_to_one")
    result["value"] = float("nan")
    valid = result.arrivals.gt(0) & result.receipts.notna()
    result.loc[valid, "value"] = result.loc[valid, "receipts"] / result.loc[valid, "arrivals"]
    result["unit"] = "current_USD_per_arrival"
    return result


def annual_variations(table):
    """Annual percent change only with a positive, observed consecutive base."""
    result = table.sort_values(["destination", "year"]).copy()
    if result.duplicated(["destination", "year"]).any():
        raise ValueError("Duplicate destination/year")
    grouped = result.groupby("destination")
    previous_year = grouped.year.shift()
    previous_value = grouped.value.shift()
    valid = result.year.sub(previous_year).eq(1) & previous_value.gt(0) & result.value.notna()
    result["variation_pct"] = float("nan")
    result.loc[valid, "variation_pct"] = 100 * (result.loc[valid, "value"] / previous_value.loc[valid] - 1)
    return result


def consecutive_segments(table, value_column="value"):
    result = table.loc[table[value_column].notna()].sort_values(["destination", "year"]).copy()
    result["segment"] = result.groupby("destination").year.transform(lambda s: s.diff().ne(1).cumsum())
    return result


def common_pre2020_summary(df, destinations):
    """Same valid annual-change years for both indicators and all selected destinations."""
    changes = pd.concat([
        annual_variations(national_series(df, layer)).assign(indicator=layer)
        for layer in ["arrivals", "receipts"]
    ], ignore_index=True)
    valid = changes.loc[changes.destination.isin(destinations) & changes.year.lt(2020) & changes.variation_pct.notna()]
    years = sorted(valid.groupby("year").size().loc[lambda s: s.eq(2 * len(destinations))].index)
    panel = valid.loc[valid.year.isin(years)]
    summary = panel.groupby(["indicator", "destination"]).variation_pct.agg(
        observations="count", median_pct="median", volatility_points="std").reset_index()
    return summary, years
