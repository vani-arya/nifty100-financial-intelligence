# Day 32 Validation Notes

## Capital Allocation Report Validation

Date: 2026-07-20

### Deliverables Validated

- output/capital_allocation_distribution.csv
- output/pattern_changes.csv
- output/cashflow_intelligence.xlsx (updated)

---

## Task 1 — Capital Allocation Coverage Validation

Source File:

- output/capital_allocation.csv

Validation Results:

- Total Rows: 1103
- Columns: 6
- Duplicate Company-Year Records Detected: 35
- Duplicate Records Removed During Analysis
- Null Values: 0

Columns Verified:

- company_id
- year
- cfo_sign
- cfi_sign
- cff_sign
- pattern_label

### Coverage Summary

- Total Companies in Platform: 92
- Companies Successfully Classified: 91
- Excluded Companies: 1

Excluded Company:

- ATGL

Reason:

ATGL has profit and balance sheet records but no cash flow records in the source database. Capital allocation classification requires operating, investing, and financing cash flow values. Therefore, classification could not be generated.

Coverage Rate:

91 / 92 = 98.9%

---

## Task 2 — Latest Capital Allocation Distribution

Methodology:

Used the latest available capital allocation record for each company.

Examples:

- ABB → Mar 2024
- TCS → Mar 2024
- SIEMENS → Sep 2024

Distribution Summary:

| Pattern | Companies |
|----------|-----------|
| Shareholder Returns | 39 |
| Reinvestor | 15 |
| Mixed | 13 |
| Growth Funded by Debt | 12 |
| Liquidating Assets | 7 |
| Unknown | 2 |
| Distress Signal | 1 |
| Pre-Revenue | 1 |

Total Classified Companies:

91

---

## Task 3 — Cash Flow Intelligence Integration

Updated:

- output/cashflow_intelligence.xlsx

Added Column:

- capital_allocation

Validation:

- Merge completed successfully
- Company IDs normalized before join
- Capital allocation classifications available for all eligible companies

---

## Task 4 — Pattern Change Analysis

Output:

- output/pattern_changes.csv

Results:

- Companies with Pattern Changes: 49

Examples:

| Company | Previous Pattern | Current Pattern |
|----------|----------------|----------------|
| ABB | Reinvestor | Shareholder Returns |
| ADANIENSOL | Mixed | Shareholder Returns |
| ADANIENT | Shareholder Returns | Mixed |
| ADANIGREEN | Shareholder Returns | Mixed |
| ASIANPAINT | Reinvestor | Shareholder Returns |

---

## Data Quality Findings

### Duplicate Records

35 duplicate company-year records were identified in the Sprint 2 capital allocation output.

Action Taken:

- Removed duplicates during Day 32 analysis
- Preserved original source file

### Fiscal Year Variations

SIEMENS follows a September reporting cycle.

Latest available record:

- Sep 2024

Analysis therefore uses latest available company record instead of enforcing a single reporting date.

### Missing Cash Flow Coverage

ATGL contains:

- Profit & Loss Data: Available
- Balance Sheet Data: Available
- Cash Flow Data: Missing

Capital allocation classification therefore cannot be computed.

---

## Risk Register Validation

### R-01 — Missing Historical Coverage

Status: Mitigated

ATGL excluded due to missing cash flow records.

### R-06 — Simulated Data Misinterpretation

Status: Passed

Capital allocation analysis performed only on available operational data.

---

## Result

PASS

Day 32 Capital Allocation Report completed successfully.

All required deliverables generated and validated.

Coverage Achieved: 91 / 92 Companies (98.9%)

Reason for exclusion fully documented and validated.