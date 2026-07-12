# Sprint 3 Retrospective — Company Screener & Peer Analytics

## Objectives Completed

- YAML-based screener configuration framework implemented
- 6 preset screeners implemented
- Composite scoring engine implemented
- Sector-relative ranking logic implemented
- Peer group mapping integrated
- Peer percentile ranking engine implemented
- peer_percentiles SQLite table populated
- Radar chart generation implemented
- Peer comparison Excel report generated
- Benchmark company highlighting implemented
- Percentile colour-coding implemented
- Peer group median calculations implemented
- Sprint 3 validation completed

## Validation Results

- Total Tests: 100 Passed, 0 Failed
- Peer Groups Processed: 11
- Peer Companies Mapped: 56
- Peer Percentile Records Generated: 550
- Radar Charts Generated: 90
- Peer Comparison Workbook: 11 Sheets
- Screener Workbook: 6 Sheets

### Screener Results

| Preset | Companies Returned |
|----------|----------|
| Quality Compounder | 21 |
| Value Pick | 2 |
| Growth Accelerator | 18 |
| Dividend Champion | 30 |
| Debt Free Bluechip | 2 |
| Turnaround Watch | 0 |

### Peer Ranking Validation

#### IT Services

| Company | ROE | Percentile Rank |
|----------|----------|----------|
| TCS | 50.94 | 1.00 |
| INFY | 29.79 | 0.80 |
| HCLTECH | 23.01 | 0.60 |
| LTIM | 22.90 | 0.40 |
| TECHM | 8.99 | 0.20 |

Validation Passed.

#### FMCG

Highest ROE company received highest percentile rank.

Lowest ROE company received lowest percentile rank.

Validation Passed.

## Edge Cases Handled

- Missing peer group assignments
- Companies without peer mappings
- Debt-to-equity inverse percentile ranking
- Missing CAGR values
- Missing KPI values
- Empty screener result sets
- Radar chart missing-value handling
- Peer-group benchmark highlighting
- Duplicate company-year observations
- Latest-year filtering before ranking

## Key Deliverables Generated

### Analytics

- src/analytics/peer.py
- src/analytics/radar.py
- src/analytics/peer_report.py

### Screener

- src/screener/engine.py
- config/screener_config.yaml
- output/screener_output.xlsx

### Peer Analytics

- peer_percentiles table
- output/peer_comparison.xlsx
- reports/radar_charts/

## Notable Findings

### SBIN Data Availability Issue

SBIN is present in:

- peer_groups.xlsx
- companies table
- profitandloss table

However, SBIN is not present in the financial_ratios table.

Since peer percentile calculations depend on KPI values sourced from financial_ratios, SBIN could not be included in percentile calculations.

This was identified as a historical KPI-generation issue rather than a Sprint 3 implementation defect.

### Screener Dataset Observation

Value Pick, Debt Free Bluechip, and Turnaround Watch returned fewer companies than the reference range specified in the guide.

Validation confirmed that screener logic and filter implementation were functioning correctly. Result counts were driven by dataset characteristics and threshold strictness rather than code defects.

## Blockers Faced

- Python import and module resolution issues during screener integration
- Missing KPI records for specific companies (SBIN)
- Peer-group mapping validation and reconciliation
- NaN propagation in percentile calculations
- Radar chart image export dependency configuration (Kaleido)
- Handling companies with incomplete historical CAGR data
- Excel workbook formatting and benchmark highlighting implementation

## Lessons Learned

- Validate source datasets before building ranking logic
- Separate business-rule validation from data-quality issues
- Perform latest-year filtering before comparative analytics
- Build validation scripts alongside implementation
- Verify peer mappings before percentile generation
- Handle missing KPI values proactively before visualisation
- Export workflows require independent validation beyond analytical logic

## Sprint 4 Preparation

- REST API development
- FastAPI endpoint implementation
- Analytics API integration
- Dashboard and frontend integration
- Performance optimisation
- End-to-end platform testing
- API documentation and deployment preparation