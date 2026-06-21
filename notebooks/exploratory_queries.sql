-- =====================================================
-- Sprint 1 Exploratory SQL Queries
-- Project: Nifty 100 Financial Intelligence Platform
-- Purpose: Database validation and exploratory analysis
-- =====================================================

-- Query 1: Row counts for major tables
SELECT 'companies' AS table_name, COUNT(*) AS row_count FROM companies
UNION ALL
SELECT 'profitandloss', COUNT(*) FROM profitandloss
UNION ALL
SELECT 'balancesheet', COUNT(*) FROM balancesheet
UNION ALL
SELECT 'cashflow', COUNT(*) FROM cashflow
UNION ALL
SELECT 'stock_prices', COUNT(*) FROM stock_prices;

--------------------------------------------------------

-- Query 2: Total companies loaded
SELECT COUNT(*) AS total_companies
FROM companies;

--------------------------------------------------------

-- Query 3: Year coverage by company
SELECT
    company_id,
    COUNT(DISTINCT year) AS years_available
FROM profitandloss
GROUP BY company_id
ORDER BY years_available DESC;

--------------------------------------------------------

-- Query 4: Companies with lowest year coverage
SELECT
    company_id,
    COUNT(DISTINCT year) AS years_available
FROM profitandloss
GROUP BY company_id
ORDER BY years_available ASC
LIMIT 10;

--------------------------------------------------------

-- Query 5: Duplicate company-year records
SELECT
    company_id,
    year,
    COUNT(*) AS duplicate_count
FROM profitandloss
GROUP BY company_id, year
HAVING COUNT(*) > 1;

--------------------------------------------------------

-- Query 6: Foreign key orphan check
SELECT COUNT(*) AS orphan_records
FROM profitandloss p
LEFT JOIN companies c
ON p.company_id = c.id
WHERE c.id IS NULL;

--------------------------------------------------------

-- Query 7: Null sales values
SELECT *
FROM profitandloss
WHERE sales IS NULL;

--------------------------------------------------------

-- Query 8: Null total assets values
SELECT *
FROM balancesheet
WHERE total_assets IS NULL;

--------------------------------------------------------

-- Query 9: Record distribution by year
SELECT
    year,
    COUNT(*) AS records
FROM profitandloss
GROUP BY year
ORDER BY year;

--------------------------------------------------------

-- Query 10: Earliest and latest year available
SELECT
    MIN(year) AS earliest_year,
    MAX(year) AS latest_year
FROM profitandloss;