# Day 20 Validation Notes

## Peer Comparison Report

- Generated peer_comparison.xlsx successfully.
- Created 11 sheets corresponding to peer groups.
- Added KPI metrics and percentile rank columns.
- Applied traffic-light percentile formatting.
- Highlighted benchmark companies using amber fill.
- Added peer-group median row at the bottom of each sheet.

## Data Quality Observation

SBIN exists in peer_groups and companies tables but is missing from financial_ratios.
As a result, KPI fields for SBIN were unavailable in the generated report.
This is a source-data issue and not a Day 20 report-generation issue.