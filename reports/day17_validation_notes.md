# Day 17 Validation Notes

## Composite Score Validation

Composite score implemented using:

- Profitability (35%)
- Cash Quality (30%)
- Growth (20%)
- Leverage (15%)

P10/P90 winsorisation applied before scaling to 0–100.

## Sector Relative Score Validation

Scores normalised within broad_sector.

Top performer in each sector receives sector score of 100.

## Screener Export Validation

Generated:

output/screener_output.xlsx

Sheets:
- Quality Compounder
- Value Pick
- Growth Accelerator
- Dividend Champion
- Debt Free Blue Chip
- Turnaround Watch

Results sorted by composite_quality_score descending.

Conditional formatting applied using green/red fills.

## Notes

Value Pick returned 2 companies.
Debt Free Blue Chip returned 2 companies.
Turnaround Watch returned 0 companies.

Screeners were implemented exactly according to project specifications without threshold relaxation.

## Data Quality Observation

During Day 17 validation, duplicate historical Free Cash Flow patterns were observed for a small number of companies (for example, ABB and ADANIENSOL) within the financial_ratios dataset.

The observation appears to originate from previously populated KPI records and does not affect the implementation logic of the composite scoring framework, sector-relative scoring, or screener export functionality developed in Day 17.

All composite score calculations were performed using the available dataset without modifying underlying historical records.

This observation has been documented for future data-quality review and dataset validation.