"""Reproducible, lightweight analysis for the Danish Housing Market project.

Run from the repository root:
    python analysis/python/analyze_housing.py

Requires: pandas (and its normal CSV dependencies).
Writes concise summary tables to analysis/outputs/.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "Housing Data.csv"
OUTPUT_DIR = ROOT / "analysis" / "outputs"


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Place the supplied CSV at data/Housing Data.csv, then rerun."
        )

    df = pd.read_csv(DATA_PATH, low_memory=False)
    required = {"date", "purchase_price", "sqm_price", "house_type", "sales_type", "region", "area", "city", "sqm"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Dataset is missing expected columns: {missing}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["purchase_price", "sqm_price", "sqm", "no_rooms", "year_build", "%_change_between_offer_and_purchase"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Dataset health and coverage.
    quality = pd.DataFrame({
        "metric": [
            "row_count", "column_count", "earliest_valid_date", "latest_valid_date",
            "duplicate_house_id_rows", "missing_date_rows", "missing_purchase_price_rows",
            "missing_sqm_price_rows", "missing_region_rows", "missing_city_rows",
        ],
        "value": [
            len(df), len(df.columns),
            df["date"].min().date().isoformat() if df["date"].notna().any() else "",
            df["date"].max().date().isoformat() if df["date"].notna().any() else "",
            int(df["house_id"].duplicated().sum()) if "house_id" in df.columns else "not available",
            int(df["date"].isna().sum()), int(df["purchase_price"].isna().sum()),
            int(df["sqm_price"].isna().sum()), int(df["region"].isna().sum()), int(df["city"].isna().sum()),
        ],
    })
    quality.to_csv(OUTPUT_DIR / "data_quality_summary.csv", index=False)

    # 2. Overall market KPIs. Mean and median use available non-null values.
    kpis = pd.DataFrame([{
        "transactions": int(len(df)),
        "total_sales_value_dkk": df["purchase_price"].sum(min_count=1),
        "average_sale_price_dkk": df["purchase_price"].mean(),
        "median_sale_price_dkk": df["purchase_price"].median(),
        "average_price_per_sqm_dkk": df["sqm_price"].mean(),
        "median_price_per_sqm_dkk": df["sqm_price"].median(),
        "average_property_size_sqm": df["sqm"].mean(),
    }])
    kpis.to_csv(OUTPUT_DIR / "market_kpis.csv", index=False)

    # 3. Annual trend table, useful for checking the Power BI trend visuals.
    dated = df.dropna(subset=["date"]).copy()
    dated["year"] = dated["date"].dt.year
    annual = dated.groupby("year", as_index=False).agg(
        homes_sold=("house_id", "count") if "house_id" in dated.columns else ("purchase_price", "count"),
        total_sales_value_dkk=("purchase_price", "sum"),
        average_sale_price_dkk=("purchase_price", "mean"),
        median_sale_price_dkk=("purchase_price", "median"),
        average_price_per_sqm_dkk=("sqm_price", "mean"),
    )
    annual["sales_value_yoy_pct"] = annual["total_sales_value_dkk"].pct_change() * 100
    annual["average_price_yoy_pct"] = annual["average_sale_price_dkk"].pct_change() * 100
    annual["price_per_sqm_yoy_pct"] = annual["average_price_per_sqm_dkk"].pct_change() * 100
    annual.to_csv(OUTPUT_DIR / "annual_market_trends.csv", index=False)

    # 4. Regional and property-type comparisons.
    region = df.groupby("region", dropna=False).agg(
        homes_sold=("purchase_price", "count"),
        total_sales_value_dkk=("purchase_price", "sum"),
        average_sale_price_dkk=("purchase_price", "mean"),
        average_price_per_sqm_dkk=("sqm_price", "mean"),
    ).reset_index()
    region["share_of_sales_value_pct"] = region["total_sales_value_dkk"] / region["total_sales_value_dkk"].sum() * 100
    region.sort_values("total_sales_value_dkk", ascending=False).to_csv(OUTPUT_DIR / "regional_comparison.csv", index=False)

    property_type = df.groupby("house_type", dropna=False).agg(
        homes_sold=("purchase_price", "count"),
        average_sale_price_dkk=("purchase_price", "mean"),
        median_sale_price_dkk=("purchase_price", "median"),
        average_price_per_sqm_dkk=("sqm_price", "mean"),
        average_size_sqm=("sqm", "mean"),
    ).reset_index()
    property_type.sort_values("homes_sold", ascending=False).to_csv(OUTPUT_DIR / "property_type_comparison.csv", index=False)

    # 5. Asking-price outcomes. Source values are percentage-point units as stored;
    # this script does not reinterpret or rescale the source field.
    offer_col = "%_change_between_offer_and_purchase"
    if offer_col in df.columns:
        offer = df[offer_col].dropna()
        outcomes = pd.DataFrame([{
            "records_with_offer_change": int(offer.size),
            "sold_below_offer_pct": float((offer < 0).mean() * 100) if offer.size else None,
            "sold_at_offer_pct": float((offer == 0).mean() * 100) if offer.size else None,
            "sold_above_offer_pct": float((offer > 0).mean() * 100) if offer.size else None,
            "mean_offer_to_purchase_change_source_units": float(offer.mean()) if offer.size else None,
            "median_offer_to_purchase_change_source_units": float(offer.median()) if offer.size else None,
        }])
        outcomes.to_csv(OUTPUT_DIR / "asking_price_outcomes.csv", index=False)

    print(f"Loaded {len(df):,} rows and {len(df.columns)} columns.")
    print(f"Date coverage: {quality.loc[2, 'value']} to {quality.loc[3, 'value']}.")
    print(f"Wrote summary CSVs to: {OUTPUT_DIR.relative_to(ROOT)}")
    print("Note: annual YoY values can be distorted by missing sales from Dec 2016 through Jun 2017 and by the partial 2024 year.")


if __name__ == "__main__":
    main()
