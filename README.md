<div align="center">

# 🇩🇰 Danish Housing Market Analysis

### An interactive Power BI report exploring a 100,000-row sample of Danish residential property sales

**Market overview · Price trends · Regional comparisons · Property insights · Buyer behaviour**

![Power BI](https://img.shields.io/badge/Power%20BI-Report-F2C811?logo=powerbi&logoColor=black)
![Power Query](https://img.shields.io/badge/Power%20Query-M-217346)
![Python](https://img.shields.io/badge/Python-pandas-3776AB?logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-SQLite-4479A1?logo=sqlite&logoColor=white)
![DAX](https://img.shields.io/badge/Analytics-DAX-4C78A8)
![Sample](https://img.shields.io/badge/Sample-100%2C000%20rows-2878C8)
![Period](https://img.shields.io/badge/Period-1992--2024-12345A)

*Portfolio project focused on turning housing transaction data into an interactive, decision-oriented report.*

</div>

---

## 📌 Project at a glance

This project analyses a 100,000-row sample of Danish housing transactions to explore how sale values and prices have changed over time, how markets differ by region and city, how property characteristics relate to pricing, and how sale outcomes compare with asking prices and interest-rate indicators.

The report contains five pages with shared filters for year range, region, area, house type and sales type. It is built with **Power BI Desktop**, **Power Query (M)** and **DAX**, using a Power BI Project (`.pbip`) structure suitable for version control.

> **Analysed sample coverage:** 100,000 transactions, from **5 January 1992 to 24 October 2024**. Amounts are presented in Danish kroner (DKK). The dataset file is not included in this repository; see [Dataset](#dataset) for access instructions.

## 🖼️ Report preview

### 1. Market Overview

![Market Overview report page](screenshots/01-market-overview.png)

**Purpose:** Answer the big-picture questions: how large is the market, what are typical sale prices, and how does current-period activity compare with the previous year?

**What it includes**
- KPI cards for total sales value, homes sold, average price, median price, price per square metre and average sale-versus-offer price.
- Annual sales value and price-per-square-metre trends.
- Sales value by region.
- Filter-aware key takeaways to summarise the selected market.

**Example reading from the supplied report:** total sales value is shown as DKK 192.6bn across 100,000 homes. The report labels 2024 comparisons as year-to-date through 24 October, compared with the same period in 2023.

### 2. Market Trends

![Market Trends report page](screenshots/02-market-trends.png)

**Purpose:** Explore the evolution of sales activity and prices over time, including growth measures and period-to-period changes.

**What it includes**
- A metric selector for sales value, homes sold, average price and price per square metre.
- Annual sales-value and year-over-year change charts.
- Quarterly price-per-square-metre trends, including average and median values.
- Monthly sales-value trends and summary growth KPIs.
- A data-reading note for incomplete or distorted periods.

**Interpretation note:** the source records no sales from **December 2016 through June 2017**. The supplied report warns that 2017 is understated and 2017–2018 changes may be distorted. The 2024 period is partial.

### 3. Regional and City Market Comparison

![Regional and City Market Comparison report page](screenshots/03-regional-city-comparison.png)

**Purpose:** Compare geography to identify where transaction value, sale prices and sales volumes are concentrated.

**What it includes**
- A configurable city ranking by selected measure.
- Controls for the number of cities displayed and minimum sales per city.
- Sales value by area and price per square metre by region.
- A summary table with homes sold, share of sales value, average price and price-per-square-metre year-over-year change.

**Questions it helps investigate:** Which areas account for the most sales value? Where are prices per square metre highest? Do high-price locations also have high transaction volumes?

### 4. Property Characteristics and Pricing

![Property Characteristics and Pricing report page](screenshots/04-property-characteristics.png)

**Purpose:** Understand how housing type, property size, number of rooms and construction era relate to transaction prices and sales volume.

**What it includes**
- Price per square metre by house type.
- Sales volume by property-size band and price band.
- Homes sold and average price by number of rooms.
- Price per square metre by year built.
- A house-type comparison table with sales volume, average price and average size.

**Questions it helps investigate:** Which property types command higher prices per square metre? Which sizes and price bands are most common? How do room count and construction period relate to pricing?

### 5. Buyer Behaviour and Interest Rates

![Buyer Behaviour and Interest Rates report page](screenshots/05-buyer-behaviour-interest-rates.png)

**Purpose:** Examine how negotiated sale prices compare with asking prices and explore how interest-rate indicators move alongside housing prices.

**What it includes**
- KPI cards for homes sold below asking price, average discount when sold below offer, auction share, interest rate, mortgage bond yield, inflation and real interest rate.
- Sale outcomes relative to asking price.
- Homes sold by sales type.
- Average sale-versus-offer price by year and annual auction share.
- Quarterly interest-rate, mortgage-bond-yield and inflation trends.
- A scatter plot comparing average annual interest rate with price per square metre.

**Interpretation note:** the interest-rate and price charts are descriptive comparisons; they do not establish that one variable caused another.

---

## 📊 Questions explored

- How have total sales value, transaction counts and housing prices changed since 1992?
- How do average price and price per square metre differ across regions, areas and cities?
- Which property types, size bands and price bands account for the most transactions?
- How often do properties sell above, at or below their asking price?
- How do interest rates, mortgage bond yields and inflation move alongside housing prices?

## 🧰 Tools and techniques

| Tool | Role in the project |
|---|---|
| **Power BI Desktop / PBIP** | Report pages, interactive filters, visuals and project structure |
| **Power Query (M)** | Importing and shaping the CSV data |
| **DAX** | Measures, calculated tables, time-based comparisons, KPI logic and rankings |
| **Python (pandas)** | Data-quality checks and summary tables to cross-check report findings |
| **SQL (SQLite-compatible)** | Queries for KPIs, annual trends, region/type comparisons, asking-price outcomes and missing macroeconomic data |
| **CSV** | Source transaction data, downloaded separately |
| **Git / GitHub** | Version control and project documentation |

## Dataset

**Source:** [Danish Residential Housing Prices 1992–2024 — Kaggle](https://www.kaggle.com/datasets/martinfrederiksen/danish-residential-housing-prices-1992-2024)

The dataset CSV is **not included** in this repository because permission to redistribute it has not been confirmed. Download the dataset from the original source and review its current terms before using it. Do not assume that the full dataset and the 100,000-row sample are interchangeable.

The Kaggle page describes approximately 1.5 million transactions in the full dataset and a separate random sample of 100,000 rows. The report screenshots and PDF document the analysed sample; use the same 100,000-row sample to reproduce the displayed figures as closely as possible.

## 📁 Repository structure

```text
Danish_housing_market_analysis/
├── Housing Market Report.pbip
├── Housing Market Report.Report/
│   └── ... report pages, visuals and theme
├── Housing Market Report.SemanticModel/
│   └── ... model, relationships, expressions and DAX tables
├── screenshots/
│   ├── 01-market-overview.png
│   ├── 02-market-trends.png
│   ├── 03-regional-city-comparison.png
│   ├── 04-property-characteristics.png
│   └── 05-buyer-behaviour-interest-rates.png
├── docs/
│   └── Housing Market Report.pdf
├── analysis/
│   ├── README.md
│   ├── analyze_housing.py
│   └── housing_analysis.sql
├── powerbi_reference/
│   ├── 1_PowerQuery_Housing_Data.m
│   ├── 2_Calculated_Tables.dax
│   └── 3_Measures.dax
├── .gitattributes
├── .gitignore
└── README.md
```

This is a guide to the intended layout. Refer to the actual files in the repository if any filenames differ.

## 🚀 Open the report

### Requirements

- Windows with a recent version of **Power BI Desktop**.
- The appropriate 100,000-row CSV sample downloaded separately from the [Kaggle source](https://www.kaggle.com/datasets/martinfrederiksen/danish-residential-housing-prices-1992-2024).

### Steps

1. Clone or download this repository and extract it.
2. Download the 100,000-row sample from the dataset source, checking the source's current terms.
3. Keep the CSV in a local folder you control. It does not need to be committed to GitHub.
4. Open `Housing Market Report.pbip` in Power BI Desktop.
5. If Power BI reports that the CSV cannot be found, open **Home → Transform data → Edit parameters** and set `CsvPath` to the full path of your downloaded CSV. For example:

   ```text
   C:\Users\YourName\Downloads\Housing Data.csv
   ```

6. Confirm the parameter, select **Close & Apply**, and allow the model to refresh.
7. Check all five report pages for refresh errors or blank visuals, then save the project.

> The exact CSV filename and column layout must match what the Power Query steps expect. If the downloaded sample differs from the one used to build the report, you may need to adjust the path or query steps.

## 🐍 Python and 🗄️ SQL analysis

The repository includes a small analysis layer to support and cross-check the Power BI report.

### Python (pandas)

The Python script is located at [`analysis/analyze_housing.py`](analysis/analyze_housing.py). It is intended to check dataset coverage and missing values, calculate overall market KPIs, create annual trends, compare regions and property types, and summarise sale outcomes against asking prices.

Run from the repository root after placing the CSV at the path expected by the script:

```bash
python -m pip install pandas
python analysis/analyze_housing.py
```

If the script expects a different CSV path, update its configuration to point to your downloaded file. Output files, if generated, depend on the script's implementation.

### SQL (SQLite-compatible)

The SQL file is located at [`analysis/housing_analysis.sql`](analysis/housing_analysis.sql). It contains focused queries for data quality, market KPIs, annual trends, regional comparisons, house types, asking-price outcomes and missing interest-rate/inflation fields. The queries expect the CSV to be imported into a SQLite table named `housing_data`, with the original column names preserved.

For example, using the SQLite command-line shell, first place the downloaded CSV at `data/Housing Data.csv` locally (the `data/` folder is not included in the repository), then run:

```sql
.mode csv
.import --skip 1 "data/Housing Data.csv" housing_data
.read analysis/housing_analysis.sql
```

If your SQLite version does not support `--skip 1`, create the table and import through a SQLite GUI such as DB Browser for SQLite, enabling the option to use the first CSV row as column names. Because the source includes punctuation in some column names, keep the original headers unchanged.

**Interpretation:** treat year-over-year changes around the December 2016–June 2017 data gap carefully, and interpret 2024 as a partial year through 24 October. The scripts do not establish causal relationships.

> **PBIP or PBIX?** This repository keeps PBIP as the main project because its report and model definitions are easier to track in Git. A PBIX is optional; it is not required to use this repository.

## 🗃️ Data quality notes

- The **analysed sample** contains 100,000 rows and is described as having 19 columns covering transaction date, property type, sales type, build year, purchase price, offer-to-purchase change, rooms, floor area, price per square metre, location and interest-rate/inflation fields. This describes the sample used for the analysis; the CSV is not hosted here.
- Coverage: **5 January 1992–24 October 2024**.
- Currency: **DKK**.
- The final year is incomplete; use same-period comparisons for 2024 where applicable.
- No sales are recorded from **December 2016 to June 2017**, affecting interpretation of 2017 and 2018 trends.
- Some macroeconomic fields contain missing values, especially near the end of the dataset. Check completeness before using those fields for new calculations.
- The PDF and screenshots are report exports for documentation. Refresh and review the PBIP report before treating the figures as newly updated results.

### Data permission

The CSV is intentionally excluded from this public repository because redistribution permission has not been confirmed. Obtain it from the original source and follow the source's applicable terms.

## 🔍 Reproducibility checklist

- [ ] Download the appropriate 100,000-row sample from the source.
- [ ] Open `Housing Market Report.pbip` in Power BI Desktop.
- [ ] Set `CsvPath` to the local CSV path if prompted.
- [ ] Refresh the model and check for errors.
- [ ] Verify all five pages and check for blank visuals.
- [ ] Review key measures and time comparisons.
- [ ] Confirm that your use of the dataset complies with its current terms.

## 📄 Included report export

A five-page PDF export is available at [`docs/Housing Market Report.pdf`](docs/Housing%20Market%20Report.pdf).

---

<div align="center">

**Built with Power BI · Power Query · DAX · Python · SQL**

*An analytical portfolio project about the Danish housing market.*

</div>
