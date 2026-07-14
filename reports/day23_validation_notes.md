# Day 23 Validation Notes

## Deliverables Completed

### Home Screen
- Implemented 6 summary KPI cards:
  - Average ROE
  - Median D/E
  - Median Revenue CAGR 5Y
  - Total Companies
  - Debt-Free Companies Count
  - Median P/E (displayed as N/A due to unavailable source data)

- Added sector distribution donut chart using Plotly.
- Added Top 5 Companies by Composite Quality Score table.
- Added year selector (2019–2024) with metric refresh support.

### Company Profile Screen
- Added company search functionality.
- Added company profile card with sector, sub-sector, ticker and business description.
- Implemented 6 financial KPI cards.
- Added Revenue vs Net Profit historical chart.
- Added ROE vs ROCE trend chart.
- Added Pros & Cons section with fallback handling when data is unavailable.
- Added user-friendly handling for unavailable company data.

## Validation Results
- Home screen KPIs rendered successfully.
- Sector distribution chart rendered correctly.
- Top company rankings displayed successfully.
- Company profile KPIs validated for multiple companies.
- Historical charts rendered correctly.
- Pros & Cons fallback verified for companies without available records.

## Observations
- P/E ratio is not available in the financial_ratios dataset and therefore is displayed as N/A.
- Pros & Cons dataset currently covers only a subset of companies.