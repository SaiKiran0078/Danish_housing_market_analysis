# Supporting analysis

This folder contains the Python and SQL analyses used to validate and explore the dataset behind the Power BI report.

## Files

- `python/analyze_housing.py` — validates expected columns and exports data-quality, KPI, annual-trend, regional, property-type and asking-price-outcome summaries.
- `sql/housing_analysis.sql` — SQL Server analysis for data quality, KPIs, annual trends, regional/city performance, property types, offer-price differences and macroeconomic indicators.

## Dataset setup

The CSV is not stored in GitHub. Download the appropriate 100,000-row sample from the [Kaggle dataset source](https://www.kaggle.com/datasets/martinfrederiksen/danish-residential-housing-prices-1992-2024), review its terms, and place the file locally at:

`data/Housing Data.csv`

Create the `data` folder in the repository root if it does not exist. The CSV is ignored by Git.

## Run the Python analysis

From the repository root:

```bash
python -m pip install pandas
python analysis/python/analyze_housing.py
```

The script creates `analysis/outputs/` and writes summary CSVs there. Those generated CSVs are intentionally ignored by Git.

## Run the SQL analysis (SQL Server / SSMS)

1. Open SQL Server Management Studio and connect to your SQL Server instance.
2. Create or select the `HOUSINGDB` database.
3. Import `data/Housing Data.csv` into `HOUSINGDB` as `dbo.[Housing Data]`, using the first CSV row as column headers.
4. Verify that the imported column names match the script, including `change_between_offer_and_purchase` for the offer-change field.
5. Open `sql/housing_analysis.sql` and execute the entire script. Review the result grids and Messages tab.

The script uses SQL Server syntax and is not SQLite-compatible. Interpret annual comparisons carefully around the December 2016–June 2017 gap in recorded sales; 2024 is partial through 24 October.
