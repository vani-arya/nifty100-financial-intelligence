# Day 21 Validation Notes

## Test Execution

Executed project test suite using pytest.

Result:

100 passed, 0 failed

This exceeds the minimum requirement of validating all DQ rules and confirms successful execution of data quality, KPI, screener, and analytics validations.

---

## Screener Validation

Generated:

output/screener_output.xlsx

Available Presets:

- quality_compounder
- value_pick
- growth_accelerator
- dividend_champion
- debt_free_bluechip
- turnaround_watch

Result Counts:

| Preset | Companies |
|----------|----------|
| Quality Compounder | 21 |
| Value Pick | 2 |
| Growth Accelerator | 18 |
| Dividend Champion | 30 |
| Debt Free Bluechip | 2 |
| Turnaround Watch | 0 |

Observation:

Value Pick, Debt Free Bluechip, and Turnaround Watch returned fewer companies than the reference range due to strict threshold conditions and current dataset characteristics.

Turnaround Watch executed successfully and exported an informational message sheet indicating that no companies matched all turnaround criteria.

---

## Peer Ranking Validation

Validated IT Services peer group:

| Company | ROE | Percentile Rank |
|----------|----------|----------|
| TCS | 50.94 | 1.00 |
| INFY | 29.79 | 0.80 |
| HCLTECH | 23.01 | 0.60 |
| LTIM | 22.90 | 0.40 |
| TECHM | 8.99 | 0.20 |

Result:

Highest ROE company received highest percentile rank.

Validation Passed.

---

## FMCG Validation

Validated FMCG peer group:

Highest ROE company (NESTLEIND) received highest percentile rank.

Lowest ROE company (GODREJCP) received lowest percentile rank.

Validation Passed.

---

## Peer Comparison Report

Generated:

output/peer_comparison.xlsx

Validation:

- 11 peer group worksheets created
- Benchmark companies highlighted
- Percentile ranks colour coded
- Peer group median row added

Validation Passed.

---

## Radar Charts

Generated radar charts for all available companies.

Location:

reports/radar_charts/

Validation Passed.

---

## Known Observation

SBIN exists in peer_groups.xlsx and source financial datasets but is not available in financial_ratios.

Peer percentile calculations depend on KPI values sourced from financial_ratios.

As a result, SBIN was excluded from percentile calculations.

This is a historical data availability issue and not a Sprint 3 implementation issue.