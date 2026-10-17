# Supporting analysis

This folder contains only the lightweight Python and SQL work used to validate and explore the same dataset behind the Power BI report.

- `python/analyze_housing.py` — data quality checks and compact KPI/trend/region/property/outcome summary exports.
- `sql/housing_analysis.sql` — SQLite-compatible analytical queries for the same core questions.

Run Python from the repository root after installing `pandas`. For SQL, import `data/Housing Data.csv` into a SQLite table named `housing_data`, preserving the CSV headers, then run the query file. Generated CSV summaries are written to `analysis/outputs/` and are intentionally git-ignored.
