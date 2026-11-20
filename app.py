"""Sales KPI dashboard.  Run:  streamlit run app.py"""
import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.data import load_sales
from dashboard.kpis import breakdown, period_delta, summarize, trend

st.set_page_config(page_title="Sales KPI Dashboard", page_icon="📈", layout="wide")


@st.cache_data
def data() -> pd.DataFrame:
    return load_sales()


df = data()

# ---- sidebar filters ----
st.sidebar.header("Filters")
min_d, max_d = df["date"].min().date(), df["date"].max().date()
picked = st.sidebar.date_input("Date range", ((pd.Timestamp(max_d) - pd.Timedelta(days=89)).date(), max_d),
                               min_value=min_d, max_value=max_d)
start, end = (picked[0], picked[-1]) if isinstance(picked, (list, tuple)) else (picked, max_d)
regions = st.sidebar.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
lines = st.sidebar.multiselect("Product line", sorted(df["product_line"].unique()),
                               default=sorted(df["product_line"].unique()))
channel = st.sidebar.radio("Channel", ["All", "Store", "Online"], horizontal=True)

f = df[df["region"].isin(regions) & df["product_line"].isin(lines)]
if channel != "All":
    f = f[f["channel"] == channel]
start_ts, end_ts = pd.Timestamp(start), pd.Timestamp(end)
cur = f[(f["date"] >= start_ts) & (f["date"] <= end_ts)]

st.title("📈 Sales KPI Dashboard")
st.caption(f"{start_ts:%d %b %Y} – {end_ts:%d %b %Y} · synthetic data")

# ---- KPI cards ----
k, d = summarize(cur), period_delta(f, start_ts, end_ts)
c1, c2, c3, c4 = st.columns(4)
fmt = lambda v: f"{v:+.1%}" if v is not None else "n/a"  # noqa: E731
c1.metric("Revenue", f"PKR {k['revenue'] / 1e6:,.1f}M", fmt(d["revenue"]))
c2.metric("Orders", f"{k['orders']:,}", fmt(d["orders"]))
c3.metric("Avg order value", f"PKR {k['aov']:,.0f}", fmt(d["aov"]))
c4.metric("Gross margin", f"{k['gross_margin']:.1%}", fmt(d["gross_margin"]))

# ---- charts ----
left, right = st.columns([2, 1])
with left:
    st.subheader("Weekly revenue by channel")
    st.plotly_chart(px.area(trend(cur), x="date", y="revenue", color="channel"), use_container_width=True)
with right:
    st.subheader("Product mix")
    st.plotly_chart(px.pie(breakdown(cur, "product_line"), names="product_line", values="revenue", hole=0.55),
                    use_container_width=True)

l2, r2 = st.columns(2)
with l2:
    st.subheader("Revenue & margin by region")
    st.plotly_chart(px.bar(breakdown(cur, "region"), x="region", y="revenue", color="margin_pct",
                           color_continuous_scale="Teal"), use_container_width=True)
with r2:
    st.subheader("Product line table")
    tbl = breakdown(cur, "product_line")
    st.dataframe(tbl.style.format({"revenue": "{:,.0f}", "cost": "{:,.0f}", "margin_pct": "{:.1%}",
                                   "share": "{:.1%}"}), use_container_width=True, hide_index=True)

st.download_button("Download filtered data (CSV)", cur.to_csv(index=False), "sales_filtered.csv", "text/csv")
