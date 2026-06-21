#checking Table count
# import sqlite3

# conn = sqlite3.connect("data/nifty100.db")

# tables = [
#     "companies",
#     "profitandloss",
#     "balancesheet",
#     "cashflow",
#     "stock_prices"
# ]

# for table in tables:
#     count = conn.execute(
#         f"SELECT COUNT(*) FROM {table}"
#     ).fetchone()[0]

#     print(f"{table}: {count}")

# conn.close()




# Which companies have very little history
# Whether the loader accidentally dropped years
# Whether there are companies with less than 5 years of data
# import sqlite3
# import pandas as pd

# conn = sqlite3.connect("data/nifty100.db")

# query = """
# SELECT
#     company_id,
#     COUNT(DISTINCT year) AS years_available
# FROM profitandloss
# GROUP BY company_id
# ORDER BY years_available;
# """

# df = pd.read_sql(query, conn)

# print(df)

# conn.close()




#Find Exactly Which Years Exist
# import sqlite3
# import pandas as pd

# conn = sqlite3.connect("data/nifty100.db")

# query = """
# SELECT
#     company_id,
#     year
# FROM profitandloss
# WHERE company_id IN (
#     'JIOFIN',
#     'LICI',
#     'ATGL',
#     'ADANIGREEN',
#     'INFY'
# )
# ORDER BY company_id, year;
# """

# df = pd.read_sql(query, conn)

# print(df)

# conn.close()




#verify there are no duplicate company-year records in the database.
# import sqlite3
# import pandas as pd

# conn = sqlite3.connect("data/nifty100.db")

# query = """
# SELECT
#     company_id,
#     year,
#     COUNT(*) AS duplicate_count
# FROM profitandloss
# GROUP BY company_id, year
# HAVING COUNT(*) > 1;
# """

# df = pd.read_sql(query, conn)

# print(df)

# conn.close()

# result:For ADANIPORTS, every year appears twice:

# Mar 2013 → 2 rows
# Mar 2014 → 2 rows
# ...
# TTM → 2 rows

# This suggests one of three possibilities:

# Possibility 1 (Most Likely)

# The source Excel itself contains duplicate records.

# Possibility 2

# The database was loaded twice accidentally.

# Possibility 3

# The loader duplicated records during processing.



#First Investigation
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

query = """
SELECT *
FROM profitandloss
WHERE company_id='ADANIPORTS'
AND year='Mar 2024';
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()



#Second Investigation:checking source file directly
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[3])
)

from src.etl.loader import load_dataset

df = load_dataset("profitandloss.xlsx")

result = df[
    (df["company_id"] == "ADANIPORTS")
    &
    (df["year"] == "Mar 2024")
]

print(result)
print("\nRows:", len(result))