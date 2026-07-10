# Day 18 Data Validation Observation

## Peer Ranking Validation

- Successfully generated peer percentile rankings across 11 peer groups and 10 ranking metrics.
- Generated 550 records in the `peer_percentiles` table.
- All percentile ranks were validated to be within the expected range of 0–1.
- D/E percentile inversion logic was verified to ensure lower debt-to-equity ratios receive higher rankings.

## Data Quality Observation

- `SBIN` is present in `peer_groups.xlsx` and the `profitandloss` table but is not available in `financial_ratios`.
- Since peer rankings depend on KPI metrics sourced from `financial_ratios`, `SBIN` was excluded from percentile ranking generation.
- This appears to be a historical data availability issue rather than a Day 18 implementation issue.

## Missing Metric Values

- A small number of percentile ranks remain null due to missing underlying CAGR metrics (primarily PAT CAGR and EPS CAGR).
- No artificial imputation was applied in order to preserve data integrity.