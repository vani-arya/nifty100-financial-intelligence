# Sprint 4 Retrospective

## Overview

Sprint 4 focused on building the end-to-end Streamlit dashboard layer for the Nifty 100 Financial Intelligence Platform. The sprint delivered 8 interactive dashboard screens, valuation analytics, peer comparison capabilities, investment screening functionality, and annual report integration.

---

## Major Deliverables

### Dashboard Screens

1. Home Dashboard
2. Company Profile
3. Financial Screener
4. Peer Comparison
5. Trend Analysis
6. Sector Analysis
7. Capital Allocation Map
8. Annual Reports

### Analytics Modules

- Peer Percentile Engine
- Screener Engine
- Valuation Engine
- Capital Allocation Classification Engine

### Outputs

- valuation_summary.xlsx
- valuation_flags.csv

---

## UX Decisions

### Screener Presets

Implemented preset-based screening:

- Quality
- Value
- Growth
- Dividend
- Debt-Free
- Turnaround

This reduced manual filter configuration effort.

### Radar Charts

Used radar visualizations for peer benchmarking because they allow quick identification of strengths and weaknesses versus peer averages.

### Treemap Visualization

Capital Allocation patterns were displayed using treemaps to provide a portfolio-level view of capital deployment behavior.

---

## Data Edge Cases Discovered

### Missing Historical Data

Several companies had limited operating history:

- JIOFIN
- LICI
- ATGL
- ADANIGREEN

Charts were adjusted to render available history without failure.

### Missing Financial Metrics

Null values existed in:

- financial_ratios
- profitandloss
- cashflow

Dashboard logic was validated to avoid crashes when values were missing.

### Median P/E KPI

Home Page Median P/E initially displayed N/A due to missing market_cap integration. Logic was corrected and validated.

---

## Performance Findings

### Profile Page Load Time

Average response time:

0.009 seconds

Requirement:

< 3 seconds

Status:

PASS

### Dashboard Stability

All 8 screens loaded successfully across tested companies without runtime failures.

---

## Lessons Learned

- Early validation of joins and key mappings prevents downstream dashboard issues.
- Defensive handling of missing data improves dashboard stability.
- Cached database queries significantly improve dashboard responsiveness.

---

## Sprint Outcome

Sprint 4 completed successfully.

All functional, performance, and QA acceptance criteria were achieved.