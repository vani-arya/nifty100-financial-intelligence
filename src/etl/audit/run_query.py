import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

query = """
SELECT COUNT(*) AS total_companies
FROM companies; 
"""

query = """
SELECT COUNT(*) AS orphan_records
FROM profitandloss p
LEFT JOIN companies c
ON p.company_id = c.id
WHERE c.id IS NULL;
"""

query = """
SELECT
    company_id,
    year,
    COUNT(*) AS duplicate_count
FROM profitandloss
GROUP BY company_id, year
HAVING COUNT(*) > 1;
"""


df = pd.read_sql(query, conn)

print(df)

conn.close()