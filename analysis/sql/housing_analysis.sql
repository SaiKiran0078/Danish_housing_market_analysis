-- Danish Housing Market Analysis — focused SQLite queries
-- Table expected: housing_data (import data/Housing Data.csv with its header row).
-- Run after importing the CSV into SQLite. Identifiers containing %, spaces, or
-- punctuation must remain double-quoted exactly as shown.

-- 1) Dataset coverage and basic quality checks
SELECT
    COUNT(*) AS transaction_rows,
    COUNT(DISTINCT house_id) AS distinct_house_ids,
    MIN(date) AS earliest_date_text,
    MAX(date) AS latest_date_text,
    SUM(CASE WHEN purchase_price IS NULL THEN 1 ELSE 0 END) AS missing_purchase_price,
    SUM(CASE WHEN sqm_price IS NULL THEN 1 ELSE 0 END) AS missing_sqm_price,
    SUM(CASE WHEN region IS NULL OR TRIM(region) = '' THEN 1 ELSE 0 END) AS missing_region
FROM housing_data;

-- 2) Overall market KPIs
SELECT
    COUNT(*) AS homes_sold,
    SUM(purchase_price) AS total_sales_value_dkk,
    AVG(purchase_price) AS average_sale_price_dkk,
    AVG(sqm_price) AS average_price_per_sqm_dkk,
    AVG(sqm) AS average_property_size_sqm
FROM housing_data;

-- 3) Annual sales value and price trends
-- The source date is stored as M/D/YYYY text. SQLite date parsing may not parse
-- that format consistently, so use the source quarter label for annual grouping.
SELECT
    CAST(SUBSTR(quarter, 1, 4) AS INTEGER) AS year,
    COUNT(*) AS homes_sold,
    SUM(purchase_price) AS total_sales_value_dkk,
    AVG(purchase_price) AS average_sale_price_dkk,
    AVG(sqm_price) AS average_price_per_sqm_dkk
FROM housing_data
GROUP BY CAST(SUBSTR(quarter, 1, 4) AS INTEGER)
ORDER BY year;

-- 4) Region comparison and sales-value share
SELECT
    region,
    COUNT(*) AS homes_sold,
    SUM(purchase_price) AS total_sales_value_dkk,
    ROUND(100.0 * SUM(purchase_price) / (SELECT SUM(purchase_price) FROM housing_data), 2) AS sales_value_share_pct,
    AVG(purchase_price) AS average_sale_price_dkk,
    AVG(sqm_price) AS average_price_per_sqm_dkk
FROM housing_data
GROUP BY region
ORDER BY total_sales_value_dkk DESC;

-- 5) House-type comparison
SELECT
    house_type,
    COUNT(*) AS homes_sold,
    AVG(purchase_price) AS average_sale_price_dkk,
    AVG(sqm_price) AS average_price_per_sqm_dkk,
    AVG(sqm) AS average_size_sqm
FROM housing_data
GROUP BY house_type
ORDER BY homes_sold DESC;

-- 6) Sale outcomes relative to asking price
-- This source column stores the offer/purchase difference as numeric values.
SELECT
    COUNT("%_change_between_offer_and_purchase") AS records_with_offer_change,
    ROUND(100.0 * SUM(CASE WHEN "%_change_between_offer_and_purchase" < 0 THEN 1 ELSE 0 END)
        / NULLIF(COUNT("%_change_between_offer_and_purchase"), 0), 2) AS sold_below_offer_pct,
    ROUND(100.0 * SUM(CASE WHEN "%_change_between_offer_and_purchase" = 0 THEN 1 ELSE 0 END)
        / NULLIF(COUNT("%_change_between_offer_and_purchase"), 0), 2) AS sold_at_offer_pct,
    ROUND(100.0 * SUM(CASE WHEN "%_change_between_offer_and_purchase" > 0 THEN 1 ELSE 0 END)
        / NULLIF(COUNT("%_change_between_offer_and_purchase"), 0), 2) AS sold_above_offer_pct,
    AVG("%_change_between_offer_and_purchase") AS average_source_value
FROM housing_data;

-- 7) Missing macroeconomic data, to assess whether rate comparisons are complete
SELECT
    COUNT(*) AS transaction_rows,
    SUM(CASE WHEN "nom_interest_rate%" IS NULL THEN 1 ELSE 0 END) AS missing_interest_rate,
    SUM(CASE WHEN "yield_on_mortgage_credit_bonds%" IS NULL THEN 1 ELSE 0 END) AS missing_bond_yield,
    SUM(CASE WHEN "dk_ann_infl_rate%" IS NULL THEN 1 ELSE 0 END) AS missing_inflation
FROM housing_data;
