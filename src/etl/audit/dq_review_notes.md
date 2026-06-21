# Day 6 Data Quality Review

## Objective

Perform a manual data quality review on the SQLite database after full ETL loading and verify year coverage, foreign key integrity, duplicate records, and loader behaviour.

## Companies Reviewed

* JIOFIN
* LICI
* ATGL
* ADANIGREEN
* INFY

## Checks Performed

### 1. Table Count Validation

Verified row counts in SQLite database against load audit report.

| Table         | Rows |
| ------------- | ---- |
| companies     | 92   |
| profitandloss | 1177 |
| balancesheet  | 1227 |
| cashflow      | 1091 |
| stock_prices  | 5520 |

Result: Passed

---

### 2. Foreign Key Integrity

Executed foreign key validation using:

PRAGMA foreign_key_check;

Result:

* FK Violations = 0

Status: Passed

---

### 3. Year Coverage Review

| Company    | Coverage   |
| ---------- | ---------- |
| JIOFIN     | 3 periods  |
| LICI       | 7 periods  |
| ATGL       | 8 periods  |
| ADANIGREEN | 9 periods  |
| INFY       | 13 periods |

Observations:

* Lower coverage companies were investigated.
* Coverage matched source datasets.
* No evidence of missing records caused by ETL processing.

Status: Passed

---

### 4. Duplicate Record Investigation

Duplicate company-year records were identified for ADANIPORTS in the profitandloss dataset.

Example:

* ADANIPORTS
* Mar 2024
* 2 identical records

Investigation Findings:

* Duplicate records exist in profitandloss.xlsx source file.
* Same duplicates are present in SQLite database.
* Loader did not create duplicates.
* Issue was previously detected by DQ-02 Annual PK Uniqueness validation.

Status:

* Source data issue
* Not a loader defect

---

## Conclusion

The ETL pipeline was manually reviewed across multiple datasets and companies.

Summary:

* Database load successful
* Row counts validated
* Foreign key integrity validated
* Year coverage validated
* Duplicate issue investigated
* No loader bugs identified

Final Result:
Day 6 Data Quality Review Passed
