from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "Housing Data.csv"
OUTPUT_DIR = ROOT / "analysis" / "outputs"

REQUIRED_COLUMNS = {
    "date", "purchase_price", "sqm_price", "house_type", "sales_type",
    "region", "area", "city", "sqm",
}
NUMERIC_COLUMNS = [
    "purchase_price",
    "sqm_price",
    "sqm",
    "no_rooms",
    "year_build",
    "%_change_between_offer_and_purchase",
]

# The source has a known gap from Dec 2016 through Jun 2017 and partial 2024 coverage.
GAP_AFFECTED_YEARS = {2016, 2017, 2018}
PARTIAL_YEARS = {2024}


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}. Place 'Housing Data.csv' in the data folder."
        )

    df = pd.read_csv(DATA_PATH, low_memory=False)
    missing = sorted(REQUIRED_COLUMNS.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def profile_data(df: pd.DataFrame) -> pd.DataFrame:
    metrics = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "earliest_valid_date": df["date"].min().date().isoformat() if df["date"].notna().any() else None,
        "latest_valid_date": df["date"].max().date().isoformat() if df["date"].notna().any() else None,
        "duplicate_house_id_rows": int(df["house_id"].duplicated().sum()) if "house_id" in df.columns else None,
        "missing_date_rows": int(df["date"].isna().sum()),
        "missing_purchase_price_rows": int(df["purchase_price"].isna().sum()),
        "missing_sqm_price_rows": int(df["sqm_price"].isna().sum()),
        "missing_region_rows": int(df["region"].isna().sum()),
        "missing_city_rows": int(df["city"].isna().sum()),
    }
    return pd.DataFrame({"metric": metrics.keys(), "value": metrics.values()})


def calculate_market_kpis(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame([{
        "transactions": int(len(df)),
        "total_sales_value_dkk": df["purchase_price"].sum(min_count=1),
        "average_sale_price_dkk": df["purchase_price"].mean(),
        "median_sale_price_dkk": df["purchase_price"].median(),
        "average_price_per_sqm_dkk": df["sqm_price"].mean(),
        "median_price_per_sqm_dkk": df["sqm_price"].median(),
        "average_property_size_sqm": df["sqm"].mean(),
    }])


def analyze_annual_trends(df: pd.DataFrame) -> pd.DataFrame:
    dated = df.dropna(subset=["date"]).copy()
    dated["year"] = dated["date"].dt.year
    volume_column = "house_id" if "house_id" in dated.columns else "purchase_price"

    annual = dated.groupby("year", as_index=False).agg(
        homes_sold=(volume_column, "count"),
        total_sales_value_dkk=("purchase_price", "sum"),
        average_sale_price_dkk=("purchase_price", "mean"),
        median_sale_price_dkk=("purchase_price", "median"),
        average_price_per_sqm_dkk=("sqm_price", "mean"),
    ).sort_values("year").reset_index(drop=True)

    for source, target in [
        ("total_sales_value_dkk", "sales_value_yoy_pct"),
        ("average_sale_price_dkk", "average_price_yoy_pct"),
        ("average_price_per_sqm_dkk", "price_per_sqm_yoy_pct"),
    ]:
        annual[target] = annual[source].pct_change(fill_method=None) * 100

    def coverage_status(year: int) -> str:
        if year in PARTIAL_YEARS:
            return "partial_year_through_2024-10-24"
        if year in GAP_AFFECTED_YEARS:
            return "affected_by_dec_2016_to_jun_2017_data_gap"
        return "no_known_coverage_issue_flagged"

    annual["coverage_status"] = annual["year"].map(coverage_status)
    annual["yoy_interpretation"] = annual["year"].apply(
        lambda year: "interpret_with_caution" if year in GAP_AFFECTED_YEARS or year in PARTIAL_YEARS
        else "standard_calendar_year_comparison"
    )
    return annual


def compare_regions(df: pd.DataFrame) -> pd.DataFrame:
    region = df.groupby("region", dropna=False).agg(
        homes_sold=("purchase_price", "count"),
        total_sales_value_dkk=("purchase_price", "sum"),
        average_sale_price_dkk=("purchase_price", "mean"),
        average_price_per_sqm_dkk=("sqm_price", "mean"),
    ).reset_index()
    total_value = region["total_sales_value_dkk"].sum()
    region["share_of_sales_value_pct"] = (
        region["total_sales_value_dkk"].div(total_value).mul(100) if total_value else pd.NA
    )
    return region.sort_values("total_sales_value_dkk", ascending=False)


def compare_property_types(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("house_type", dropna=False).agg(
        homes_sold=("purchase_price", "count"),
        average_sale_price_dkk=("purchase_price", "mean"),
        median_sale_price_dkk=("purchase_price", "median"),
        average_price_per_sqm_dkk=("sqm_price", "mean"),
        average_size_sqm=("sqm", "mean"),
    ).reset_index().sort_values("homes_sold", ascending=False)


def analyze_offer_change(df: pd.DataFrame) -> pd.DataFrame | None:
    column = "%_change_between_offer_and_purchase"
    if column not in df.columns:
        return None

    values = df[column].dropna()
    if values.empty:
        return pd.DataFrame([{
            "records_with_offer_change": 0,
            "negative_change_pct": None,
            "zero_change_pct": None,
            "positive_change_pct": None,
            "mean_change_source_units": None,
            "median_change_source_units": None,
        }])

    # Avoid assigning business meaning to the sign until the source field definition is confirmed.
    return pd.DataFrame([{
        "records_with_offer_change": int(values.size),
        "negative_change_pct": float(values.lt(0).mean() * 100),
        "zero_change_pct": float(values.eq(0).mean() * 100),
        "positive_change_pct": float(values.gt(0).mean() * 100),
        "mean_change_source_units": float(values.mean()),
        "median_change_source_units": float(values.median()),
    }])


def main() -> None:
    df = load_data()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    quality = profile_data(df)
    outputs = {
        "data_quality_summary.csv": quality,
        "market_kpis.csv": calculate_market_kpis(df),
        "annual_market_trends.csv": analyze_annual_trends(df),
        "regional_comparison.csv": compare_regions(df),
        "property_type_comparison.csv": compare_property_types(df),
    }
    offer_change = analyze_offer_change(df)
    if offer_change is not None:
        outputs["asking_price_outcomes.csv"] = offer_change

    for filename, result in outputs.items():
        result.to_csv(OUTPUT_DIR / filename, index=False)

    start_date = quality.loc[quality["metric"].eq("earliest_valid_date"), "value"].iloc[0]
    end_date = quality.loc[quality["metric"].eq("latest_valid_date"), "value"].iloc[0]
    print(f"Rows: {len(df):,} | Columns: {len(df.columns):,}")
    print(f"Date coverage: {start_date} to {end_date}")
    print(f"Analysis outputs: {OUTPUT_DIR.relative_to(ROOT)} ({len(outputs)} files)")
    print("Annual YoY values are retained, with coverage flags for the 2016–2018 data gap and partial 2024 year.")
    print("Offer-change results describe negative/zero/positive source values; business interpretation requires source-field documentation.")


if __name__ == "__main__":
    main()
