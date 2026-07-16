# NIFTY100 Financial Intelligence Platform

Financial analytics and investment research platform built on Nifty 100 companies. The platform combines financial statement analytics, valuation models, investment screening, peer benchmarking, sector analysis, capital allocation insights, and annual report access through an interactive Streamlit dashboard.

---

## Features

- Financial analytics for 92 Nifty 100 companies
- 50+ financial KPIs
- Interactive Streamlit dashboard
- Peer comparison engine
- Financial screener with presets
- Sector analytics
- Capital allocation classification
- Valuation engine with overvaluation flags
- Annual report explorer
- SQLite-powered analytics backend

---

## Tech Stack

- Python
- SQLite
- Pandas
- NumPy
- Streamlit
- Plotly
- OpenPyXL
- ReportLab

---

## Project Structure

```text
src/
│
├── analytics/
├── dashboard/
│   ├── pages/
│   └── utils/
│
├── screener/
├── peer_analysis/
├── capital_allocation/
│
data/
db/
output/
reports/
tests/
config/
```

---

## Running the Dashboard

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch Dashboard

```bash
streamlit run src/dashboard/app.py
```

---

## Dashboard Screens

### 1. Home Dashboard

Provides platform-wide insights and key financial metrics including:

- Average ROE
- Median Debt-to-Equity
- Median Revenue CAGR
- Median P/E Ratio
- Debt-Free Company Count

---

### 2. Company Profile

Detailed company-level analysis including:

- Financial KPIs
- Growth Metrics
- Profitability Metrics
- Balance Sheet Insights
- Pros & Cons Summary

---

### 3. Financial Screener

Interactive filtering using:

- ROE
- Debt-to-Equity
- Free Cash Flow
- Revenue CAGR
- PAT CAGR
- Operating Margin
- P/E Ratio
- P/B Ratio
- Dividend Yield
- Interest Coverage

#### Preset Screeners

- Quality
- Value
- Growth
- Dividend
- Debt-Free
- Turnaround

---

### 4. Peer Comparison

- Peer Group Benchmarking
- Radar Chart Visualization
- Peer Average Comparison
- Benchmark Company Identification

---

### 5. Trend Analysis

- Historical KPI Trends
- Multi-Metric Comparison
- YoY Growth Analysis
- 10-Year Financial Visualization

---

### 6. Sector Analysis

- Sector-Level Analytics
- Revenue vs ROE Bubble Charts
- Market-Cap Weighted Insights
- Sector Median KPI Comparison

---

### 7. Capital Allocation Map

Classification of companies into:

- Capital Compounder
- Cash Generator
- Capital Intensive
- Aggressive Reinvestor
- Dividend Machine
- Debt Reducer
- Debt Free
- Turnaround Builder

---

### 8. Annual Reports

- Company-wise Annual Reports
- Historical Report Archive
- Direct BSE Report Access

---

## Valuation Module

Implemented in:

```text
src/analytics/valuation.py
```

### Features

- FCF Yield Calculation
- Sector Median P/E Benchmarking
- Valuation Flagging
- Overvaluation Detection

### Generated Outputs

```text
output/valuation_summary.xlsx
output/valuation_flags.csv
```

---

## Sprint 4 Deliverables

### Dashboard

- Home Dashboard
- Company Profile
- Financial Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation Map
- Annual Reports

### Analytics

- Peer Percentile Engine
- Screener Engine
- Valuation Engine
- Capital Allocation Engine

### Outputs

- valuation_summary.xlsx
- valuation_flags.csv

---

## Performance Validation

### QA Results

- All 8 screens validated
- 92 companies supported
- Partial-data companies supported
- Screener stress-tested
- Missing-value handling validated

### Load Time

Average Company Profile Load Time:

```text
0.009 seconds
```

Requirement:

```text
< 3 seconds
```

Status:

```text
PASS
```

---

## Sprint Status

| Sprint | Status |
|---------|---------|
| Sprint 1 | Completed |
| Sprint 2 | Completed |
| Sprint 3 | Completed |
| Sprint 4 | Completed |

---

## Author

Developed as part of the Bluestock Fintech Data Analytics Program.
