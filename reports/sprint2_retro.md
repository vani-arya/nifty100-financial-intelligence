# Sprint 2 Retrospective — Financial Ratio Engine

## Objectives Completed

- Profitability ratios implemented
- Leverage ratios implemented
- CAGR engine implemented
- Cash flow KPI engine implemented
- Capital allocation classification implemented
- financial_ratios table populated
- ROCE validation completed
- ROE validation completed
- Edge case logging completed

## Validation Results

- financial_ratios rows: 1160
- KPI Tests: 46 Passed, 0 Failed
- KPI columns populated successfully
- ROCE validation completed
- ROE validation completed

## Edge Cases Handled

- Negative equity
- Zero sales
- Debt-free companies
- Financial sector D/E carve-out
- CAGR turnaround
- CAGR decline-to-loss
- CAGR zero-base
- Division-by-zero protection

## Screener Validation Finding

The screener was tested using:

ROE > 15%
D/E < 1
FCF > 0

Historical-year query returned 381 records due to multiple company-year observations.

Latest-year query returned 1 company (SIEMENS).

The screener logic was validated successfully. Result count reflects dataset characteristics and KPI distributions rather than formula defects.

## Blockers Faced

- Duplicate company-year records during ROCE validation
- ROCE mismatches vs source values
- Financial-sector treatment
- TCS ROE source anomaly

## Lessons Learned

- Validate source metrics early
- Check joins for duplicates
- Maintain anomaly logs
- Handle sector-specific formulas separately

## Sprint 3 Preparation

- API layer
- Screener endpoints
- Sector benchmarking
- Peer comparison analytics