# Day 36 Validation Notes

## Task
KMeans Clustering

---

## Objective

Cluster all 92 companies into 5 financial archetypes using:

- Return on Equity
- Debt to Equity
- Revenue CAGR (5Y)
- FCF CAGR (5Y)
- Operating Profit Margin

---

## Data Preparation

### Sources

- financial_ratios table
- sectors table
- cashflow_intelligence.xlsx

### Processing

- Latest company snapshot selected
- Sector-median imputation applied
- Global median fallback applied
- Outlier capping applied
- StandardScaler normalization applied

---

## Scaling Validation

Feature Means:

```text
[-0. -0. -0.  0.  0.]
```

Feature Standard Deviations:

```text
[1. 1. 1. 1. 1.]
```

Status: PASS

---

## Clustering Configuration

```python
KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)
```

Status: PASS

---

## Companies Clustered

Total Companies: 92

Status: PASS

---

## Cluster Distribution

| Cluster | Count |
|----------|--------|
| Defensive Dividend | 39 |
| Emerging Growth | 26 |
| Value Cyclicals | 12 |
| High-Quality Growth | 11 |
| Distressed | 4 |

Status: PASS

---

## Cluster Profiles

| Cluster | ROE | D/E | Revenue CAGR | FCF CAGR | OPM |
|----------|------|------|------|------|------|
| Emerging Growth | 17.12 | 0.71 | 16.89 | -3.45 | 24.69 |
| High-Quality Growth | 59.34 | 0.59 | 11.85 | 13.38 | 42.27 |
| Defensive Dividend | 16.32 | 0.48 | 7.81 | 15.89 | 34.46 |
| Value Cyclicals | 17.60 | 6.15 | 18.23 | -19.88 | 80.50 |
| Distressed | 15.76 | 6.19 | 17.73 | -26.16 | -45.00 |

---

## Outputs Generated

reports/elbow_plot.png

output/cluster_labels.csv

output/cluster_profiles.csv

---

## Final Status

Day 36 Status: COMPLETED

All 92 companies assigned to one of 5 archetypes.

Ready for Day 37.