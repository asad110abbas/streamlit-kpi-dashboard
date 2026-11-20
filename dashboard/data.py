"""Synthetic daily sales by product line, region and channel."""
from __future__ import annotations

import numpy as np
import pandas as pd


def load_sales(days: int = 730, seed: int = 21) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp("2025-12-31"), periods=days, freq="D")
    lines = {"Mobiles": 900, "Laptops": 450, "Audio": 300, "Wearables": 200, "Accessories": 350}
    regions, channels = ["North", "South", "East", "West"], ["Store", "Online"]
    rows = []
    for line, base in lines.items():
        for region in regions:
            for channel in channels:
                t = np.arange(days)
                season = 1 + 0.2 * np.sin(2 * np.pi * t / 365) + 0.3 * dates.month.isin([11, 12])
                growth = 1 + 0.0005 * t * (1.6 if channel == "Online" else 0.8)
                orders = rng.poisson(base / 8 * season * growth)
                aov = rng.normal({"Mobiles": 60000, "Laptops": 180000, "Audio": 9000, "Wearables": 22000,
                                  "Accessories": 2500}[line], 800, days).clip(500)
                rows.append(pd.DataFrame({"date": dates, "product_line": line, "region": region, "channel": channel,
                                          "orders": orders, "revenue": (orders * aov).round(0),
                                          "cost": (orders * aov * rng.uniform(.65, .8)).round(0)}))
    return pd.concat(rows, ignore_index=True)
