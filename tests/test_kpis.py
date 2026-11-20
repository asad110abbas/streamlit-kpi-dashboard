import pandas as pd
import pytest

from dashboard.data import load_sales
from dashboard.kpis import breakdown, period_delta, summarize


def test_summarize_basic():
    df = pd.DataFrame({"revenue": [100.0, 300.0], "cost": [60.0, 140.0], "orders": [1, 3]})
    k = summarize(df)
    assert k == {"revenue": 400.0, "orders": 4, "aov": 100.0, "gross_margin": pytest.approx(0.5)}


def test_summarize_empty_is_safe():
    k = summarize(pd.DataFrame({"revenue": [], "cost": [], "orders": []}))
    assert k["aov"] == 0 and k["gross_margin"] == 0


def test_period_delta_doubles():
    dates = pd.date_range("2025-01-01", periods=20)
    df = pd.DataFrame({"date": dates, "revenue": [10.0] * 10 + [20.0] * 10, "cost": 0.0, "orders": 1})
    d = period_delta(df, dates[10], dates[19])
    assert d["revenue"] == pytest.approx(1.0)


def test_breakdown_shares_sum_to_one():
    b = breakdown(load_sales(days=60), "region")
    assert b["share"].sum() == pytest.approx(1.0)
