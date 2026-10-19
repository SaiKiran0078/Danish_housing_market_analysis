/* Danish Housing Market Analysis | SQL Server */

IF DB_ID(N'HOUSINGDB') IS NULL
    CREATE DATABASE [HOUSINGDB];
GO

USE [HOUSINGDB];
GO

SET NOCOUNT ON;

IF OBJECT_ID(N'dbo.Housing Data', N'U') IS NULL
BEGIN
    RAISERROR('dbo.[Housing Data] was not found in HOUSINGDB. Import the dataset before running the analysis.', 16, 1);
    RETURN;
END;
GO

-- 1. DATA QUALITY
SELECT
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = N'dbo'
  AND TABLE_NAME = N'Housing Data'
ORDER BY ORDINAL_POSITION;

SELECT
    COUNT_BIG(*) AS total_rows,
    COUNT(DISTINCT house_id) AS distinct_house_ids,
    SUM(CASE WHEN [date] IS NULL OR LTRIM(RTRIM([date])) = N'' THEN 1 ELSE 0 END) AS missing_date,
    SUM(CASE WHEN purchase_price IS NULL THEN 1 ELSE 0 END) AS missing_purchase_price,
    SUM(CASE WHEN sqm_price IS NULL THEN 1 ELSE 0 END) AS missing_sqm_price,
    SUM(CASE WHEN sqm IS NULL OR sqm <= 0 THEN 1 ELSE 0 END) AS missing_or_invalid_size,
    SUM(CASE WHEN region IS NULL OR LTRIM(RTRIM(region)) = N'' THEN 1 ELSE 0 END) AS missing_region,
    SUM(CASE WHEN city IS NULL OR LTRIM(RTRIM(city)) = N'' THEN 1 ELSE 0 END) AS missing_city,
    SUM(CASE WHEN change_between_offer_and_purchase IS NULL
              OR LTRIM(RTRIM(change_between_offer_and_purchase)) = N'' THEN 1 ELSE 0 END) AS missing_offer_change
FROM dbo.[Housing Data];

SELECT house_id, COUNT_BIG(*) AS rows_per_house_id
FROM dbo.[Housing Data]
GROUP BY house_id
HAVING COUNT_BIG(*) > 1
ORDER BY rows_per_house_id DESC;

-- 2. ANALYTICAL DATASET
IF OBJECT_ID('tempdb..#Housing') IS NOT NULL DROP TABLE #Housing;

SELECT
    COALESCE(
        TRY_CONVERT(date, [date], 101),
        TRY_CONVERT(date, [date], 23),
        TRY_CONVERT(date, [date], 120),
        TRY_CONVERT(date, [date], 103)
    ) AS sale_date,
    TRY_CONVERT(int, LEFT(LTRIM(RTRIM([quarter])), 4)) AS quarter_year,
    house_id,
    NULLIF(LTRIM(RTRIM(house_type)), N'') AS house_type,
    NULLIF(LTRIM(RTRIM(sales_type)), N'') AS sales_type,
    TRY_CONVERT(int, year_build) AS year_build,
    TRY_CONVERT(decimal(19,2), purchase_price) AS purchase_price,
    TRY_CONVERT(float, change_between_offer_and_purchase) AS offer_purchase_change,
    TRY_CONVERT(float, no_rooms) AS no_rooms,
    TRY_CONVERT(float, sqm) AS sqm,
    TRY_CONVERT(float, sqm_price) AS sqm_price,
    NULLIF(LTRIM(RTRIM(city)), N'') AS city,
    NULLIF(LTRIM(RTRIM(area)), N'') AS area,
    NULLIF(LTRIM(RTRIM(region)), N'') AS region,
    TRY_CONVERT(float, nom_interest_rate) AS nominal_interest_rate,
    TRY_CONVERT(float, dk_ann_infl_rate) AS annual_inflation_rate,
    TRY_CONVERT(float, yield_on_mortgage_credit_bonds) AS mortgage_bond_yield
INTO #Housing
FROM dbo.[Housing Data];

SELECT
    COUNT_BIG(*) AS total_rows,
    MIN(sale_date) AS earliest_sale_date,
    MAX(sale_date) AS latest_sale_date,
    SUM(CASE WHEN sale_date IS NULL THEN 1 ELSE 0 END) AS unparsed_dates,
    SUM(CASE WHEN purchase_price IS NULL THEN 1 ELSE 0 END) AS unparsed_purchase_prices,
    SUM(CASE WHEN sqm_price IS NULL THEN 1 ELSE 0 END) AS unparsed_sqm_prices
FROM #Housing;

-- 3. MARKET OVERVIEW
SELECT
    COUNT_BIG(*) AS transactions,
    SUM(purchase_price) AS total_sales_value_dkk,
    AVG(purchase_price) AS average_sale_price_dkk,
    AVG(sqm_price) AS average_price_per_sqm_dkk,
    AVG(sqm) AS average_property_size_sqm
FROM #Housing;

-- 4. ANNUAL TRENDS AND YEAR-OVER-YEAR GROWTH
WITH Annual AS (
    SELECT
        COALESCE(YEAR(sale_date), quarter_year) AS [year],
        COUNT_BIG(*) AS transactions,
        SUM(purchase_price) AS total_sales_value_dkk,
        AVG(purchase_price) AS average_sale_price_dkk,
        AVG(sqm_price) AS average_price_per_sqm_dkk
    FROM #Housing
    WHERE COALESCE(YEAR(sale_date), quarter_year) IS NOT NULL
    GROUP BY COALESCE(YEAR(sale_date), quarter_year)
),
Trend AS (
    SELECT *,
        LAG(transactions) OVER (ORDER BY [year]) AS previous_transactions,
        LAG(total_sales_value_dkk) OVER (ORDER BY [year]) AS previous_sales_value,
        LAG(average_sale_price_dkk) OVER (ORDER BY [year]) AS previous_average_price
    FROM Annual
)
SELECT *,
    100.0 * (transactions - previous_transactions)
        / NULLIF(previous_transactions, 0) AS transactions_yoy_pct,
    100.0 * (total_sales_value_dkk - previous_sales_value)
        / NULLIF(previous_sales_value, 0) AS sales_value_yoy_pct,
    100.0 * (average_sale_price_dkk - previous_average_price)
        / NULLIF(previous_average_price, 0) AS average_price_yoy_pct
FROM Trend
ORDER BY [year];

-- 5. REGIONAL AND CITY PERFORMANCE
SELECT
    region,
    COUNT_BIG(*) AS transactions,
    SUM(purchase_price) AS total_sales_value_dkk,
    AVG(purchase_price) AS average_sale_price_dkk,
    AVG(sqm_price) AS average_price_per_sqm_dkk
FROM #Housing
GROUP BY region
ORDER BY total_sales_value_dkk DESC;

SELECT
    city,
    region,
    COUNT_BIG(*) AS transactions,
    SUM(purchase_price) AS total_sales_value_dkk,
    AVG(purchase_price) AS average_sale_price_dkk,
    AVG(sqm_price) AS average_price_per_sqm_dkk
FROM #Housing
WHERE city IS NOT NULL
GROUP BY city, region
HAVING COUNT_BIG(*) >= 30
ORDER BY total_sales_value_dkk DESC;

-- 6. PROPERTY TYPE AND SALES CHANNEL
SELECT
    house_type,
    COUNT_BIG(*) AS transactions,
    AVG(purchase_price) AS average_sale_price_dkk,
    AVG(sqm_price) AS average_price_per_sqm_dkk,
    AVG(sqm) AS average_size_sqm,
    AVG(no_rooms) AS average_rooms
FROM #Housing
GROUP BY house_type
ORDER BY transactions DESC;

SELECT
    sales_type,
    COUNT_BIG(*) AS transactions,
    AVG(purchase_price) AS average_sale_price_dkk,
    AVG(offer_purchase_change) AS average_offer_purchase_change
FROM #Housing
GROUP BY sales_type
ORDER BY transactions DESC;

-- 7. OFFER-TO-PURCHASE PRICE DIFFERENCES
SELECT
    COUNT(offer_purchase_change) AS rows_with_offer_change,
    SUM(CASE WHEN offer_purchase_change < 0 THEN 1 ELSE 0 END) AS negative_change_rows,
    SUM(CASE WHEN offer_purchase_change = 0 THEN 1 ELSE 0 END) AS zero_change_rows,
    SUM(CASE WHEN offer_purchase_change > 0 THEN 1 ELSE 0 END) AS positive_change_rows,
    AVG(offer_purchase_change) AS average_offer_purchase_change
FROM #Housing;

-- 8. HOUSING PRICES AND MACROECONOMIC INDICATORS
SELECT
    COALESCE(YEAR(sale_date), quarter_year) AS [year],
    AVG(nominal_interest_rate) AS average_nominal_interest_rate,
    AVG(mortgage_bond_yield) AS average_mortgage_bond_yield,
    AVG(annual_inflation_rate) AS average_annual_inflation_rate,
    AVG(purchase_price) AS average_sale_price_dkk,
    AVG(sqm_price) AS average_price_per_sqm_dkk
FROM #Housing
WHERE COALESCE(YEAR(sale_date), quarter_year) IS NOT NULL
GROUP BY COALESCE(YEAR(sale_date), quarter_year)
ORDER BY [year];



-- 9. CLEANUP
DROP TABLE IF EXISTS #Housing;

