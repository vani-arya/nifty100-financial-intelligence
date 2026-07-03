# Day 12 Validation Notes

## financial_ratios Table

- Row Count: 1160
- Added Columns:
  - revenue_cagr_5yr
  - pat_cagr_5yr
  - eps_cagr_5yr
  - composite_quality_score

## Validation

- KPI columns populated successfully
- CAGR calculations generated successfully
- Composite quality score calculated successfully

## Observations

- Duplicate company-year records detected in financial_ratios
- Examples: PNB (5 duplicates), ABB (2 duplicates)
- Duplicates appear to originate from source tables and will be reviewed in subsequent DQ checks