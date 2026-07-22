import sqlite3
import pandas as pd
import numpy as np

from pathlib import Path

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt

def load_latest_ratios():

    conn = sqlite3.connect(
        "data/nifty100.db"
    )

    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )

    sectors = pd.read_sql(
        """
        SELECT
            company_id,
            broad_sector
        FROM sectors
        """,
        conn
    )

    conn.close()

    ratios = (
        ratios
        .sort_values("year")
        .groupby("company_id")
        .tail(1)
    )

    ratios = ratios.merge(
        sectors,
        on="company_id",
        how="right"
    )

    return ratios


def load_cashflow():

    return pd.read_excel(
        "output/cashflow_intelligence.xlsx"
    )[
        [
            "company_id",
            "fcf_cagr_5yr"
        ]
    ]


df = load_latest_ratios()

cashflow = load_cashflow()

df = df.merge(
    cashflow,
    on="company_id",
    how="left"
)

print(
    "Companies:",
    df["company_id"].nunique()
)


features = [

    "return_on_equity_pct",

    "debt_to_equity",

    "revenue_cagr_5yr",

    "fcf_cagr_5yr",

    "operating_profit_margin_pct"
]


for feature in features:

    df[feature] = (
        df.groupby(
            "broad_sector"
        )[feature]
        .transform(
            lambda x:
            x.fillna(
                x.median()
            )
        )
    )

for feature in features:

    df[feature] = (
        df[feature]
        .fillna(
            df[feature].median()
        )
    )


# Remove extreme outliers

df["return_on_equity_pct"] = (
    df["return_on_equity_pct"]
    .clip(-50, 100)
)

df["operating_profit_margin_pct"] = (
    df["operating_profit_margin_pct"]
    .clip(-100, 100)
)

df["revenue_cagr_5yr"] = (
    df["revenue_cagr_5yr"]
    .clip(-50, 100)
)

df["fcf_cagr_5yr"] = (
    df["fcf_cagr_5yr"]
    .clip(-100, 200)
)

df["debt_to_equity"] = (
    df["debt_to_equity"]
    .clip(0, 10)
)


for feature in features:

    lower = (
        df[feature]
        .quantile(0.05)
    )

    upper = (
        df[feature]
        .quantile(0.95)
    )

    df[feature] = (
        df[feature]
        .clip(
            lower=lower,
            upper=upper
        )
    )

print("\nFeature Summary After Winsorization")

print(
    df[features]
    .describe()
)

scaler = StandardScaler()

X_scaled = scaler.fit_transform(
    df[features]
)

print(
    np.round(
        X_scaled.mean(axis=0),
        3
    )
)

print(
    np.round(
        X_scaled.std(axis=0),
        3
    )
)


inertia = []

for k in range(2, 11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)

    inertia.append(
        model.inertia_
    )


plt.figure(figsize=(8,5))

plt.plot(
    range(2,11),
    inertia,
    marker="o"
)

plt.title(
    "Elbow Plot"
)

plt.xlabel("K")

plt.ylabel("Inertia")

Path("reports").mkdir(
    exist_ok=True
)

plt.savefig(
    "reports/elbow_plot.png"
)

plt.close()


kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

df["cluster_id"] = (
    kmeans.fit_predict(
        X_scaled
    )
)


distances = (
    kmeans.transform(
        X_scaled
    )
)

df[
    "distance_from_centroid"
] = distances.min(
    axis=1
)


cluster_map = {

    0: "Emerging Growth",

    1: "High-Quality Compounders",

    2: "Defensive Dividend Payers",

    3: "Value Cyclicals",

    4: "Distressed Turnaround"
}

df["cluster_name"] = (
    df["cluster_id"]
    .map(cluster_map)
)


labels = df[
    [
        "company_id",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid"
    ]
]

Path("output").mkdir(
    exist_ok=True
)

labels.to_csv(
    "output/cluster_labels.csv",
    index=False
)


cluster_mean = (
    df.groupby(
        "cluster_id"
    )[features]
    .mean()
    .round(2)
)

cluster_median = (
    df.groupby(
        "cluster_id"
    )[features]
    .median()
    .round(2)
)

cluster_mean.to_csv(
    "output/cluster_profiles_mean.csv"
)

cluster_median.to_csv(
    "output/cluster_profiles_median.csv"
)


print(
    "\nCluster Counts"
)

print(
    df["cluster_id"]
    .value_counts()
)

print(
    "\nFiles Generated:"
)

print(
    "reports/elbow_plot.png"
)

print(
    "output/cluster_labels.csv"
)

print(
    "output/cluster_profiles.csv"
)