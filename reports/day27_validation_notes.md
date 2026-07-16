# Sprint 4 Day 27 – Integration QA & Bug Fixes

## Completed

- Performed end-to-end QA validation across all 8 Streamlit dashboard screens.
- Validated Home, Profile, Screener, Peer Comparison, Trend Analysis, Sector Analysis, Capital Allocation, and Annual Reports pages.
- Fixed Home Page KPI issue where Median P/E was displaying as N/A despite market_cap data being available.
- Added dynamic Median P/E calculation using latest valuation data.
- Verified dashboard stability under normal and edge-case scenarios.
- Confirmed all pages load successfully without runtime errors.

---

## QA Tests Performed

### 1. Multi-Sector Company Testing

Tested dashboard functionality using companies across multiple sectors:

- TCS
- INFY
- HDFCBANK
- ICICIBANK
- ITC
- HINDUNILVR
- RELIANCE
- ONGC
- SUNPHARMA
- APOLLOHOSP

### Result

PASS

All screens loaded successfully for all tested companies.

---

### 2. Company Profile Load Time Testing

Measured Company Profile page response times.

| Company | Load Time (s) |
|----------|----------|
| TCS | 0.072 |
| INFY | 0.002 |
| HDFCBANK | 0.002 |
| ICICIBANK | 0.002 |
| ITC | 0.002 |
| HINDUNILVR | 0.003 |
| RELIANCE | 0.002 |
| ONGC | 0.003 |
| SUNPHARMA | 0.002 |
| APOLLOHOSP | 0.002 |

Average Load Time: **0.009 seconds**

### Result

PASS

Requirement: < 3 seconds

---

### 3. Partial Data Validation

Companies with limited historical data were tested:

- JIOFIN (3 years)
- LICI (7 years)
- ATGL (8 years)
- ADANIGREEN (9 years)

Validated on:

- Company Profile
- Trend Analysis
- Annual Reports

### Result

PASS

No crashes observed. Charts rendered successfully with available data.

---

### 4. Screener Stress Testing

Test Cases:

#### Minimum Filter Values

- All filters set to lowest possible values

#### Maximum Filter Values

- All filters set to strictest possible values

### Result

PASS

No crashes, errors, or unexpected behavior observed.

---

### 5. Chart Layout Validation

Validated chart rendering on:

- Profile Page
- Peer Comparison Page
- Trend Analysis Page
- Sector Analysis Page
- Capital Allocation Page

Checks Performed:

- No horizontal overflow
- No clipping
- No chart truncation
- Responsive page rendering

### Result

PASS

---

### 6. Missing Data Validation

Verified handling of datasets containing null values:

| Table | Null Cells |
|---------|---------|
| financial_ratios | 1831 |
| market_cap | 0 |
| profitandloss | 215 |
| cashflow | 8 |

### Result

PASS

Dashboard handled missing values without crashing.

---

## Bugs Fixed

### Home Page KPI Bug

Issue:

- Median P/E displayed as N/A.

Resolution:

- Added market_cap integration into Home Page KPI calculations.
- Implemented dynamic Median P/E computation.

Result:

- Median P/E now displays correctly.

---

## Final Validation Summary

| Validation Area | Status |
|----------------|---------|
| Home Page | PASS |
| Company Profile | PASS |
| Financial Screener | PASS |
| Peer Comparison | PASS |
| Trend Analysis | PASS |
| Sector Analysis | PASS |
| Capital Allocation | PASS |
| Annual Reports | PASS |
| Load Time Testing | PASS |
| Partial Data Testing | PASS |
| Missing Data Handling | PASS |
| UI Layout Validation | PASS |

---

## Status

Sprint 4 Day 27 completed successfully.

All dashboard modules, analytics modules, visualization screens, and validation checks passed QA testing requirements.