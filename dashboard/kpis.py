"""Pure KPI functions (unit-tested separately from the UI)."""
from __future__ import annotations

import pandas as pd


def summarize(df: pd.DataFrame) -> dict:
    revenue, cost, orders = df["revenue"].sum(), df["cost"].sum(), df["orders"].sum()
    return {
        "revenue": float(revenue),
        "orders": int(orders),
        "aov": float(revenue / orders) if orders else 0.0,
        "gross_margin": float((revenue - cost) / revenue) if revenue else 0.0,
    }


def period_delta(df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> dict:
    """KPI change vs. the immediately preceding period of equal length."""
    length = end - start
    cur = df[(df["date"] >= start) & (df["date"] <= end)]
    prev = df[(df["date"] >= start - length - pd.Timedelta(days=1)) & (df["date"] < start)]
    a, b = summarize(cur), summarize(prev)
    return {k: (a[k] - b[k]) / b[k] if b[k] else None for k in a}


def trend(df: pd.DataFrame, freq: str = "W") -> pd.DataFrame:
    return (df.set_index("date").groupby([pd.Grouper(freq=freq), "channel"])["revenue"].sum()
            .reset_index())


def breakdown(df: pd.DataFrame, by: str) -> pd.DataFrame:
    g = df.groupby(by)[["revenue", "cost", "orders"]].sum()
    g["margin_pct"] = (g["revenue"] - g["cost"]) / g["revenue"]
    g["share"] = g["revenue"] / g["revenue"].sum()
    return g.sort_values("revenue", ascending=False).reset_index()
