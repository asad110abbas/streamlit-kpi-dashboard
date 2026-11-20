# 📈 BRIHA · Streamlit Sales KPI Dashboard

![BRIHA](https://img.shields.io/badge/BRIHA-Genesis_of_AGI-8B5CF6?style=for-the-badge&labelColor=0B1024) ![Module](https://img.shields.io/badge/Briha-Data_Lab-00F0FF?style=for-the-badge&labelColor=0B1024)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)
![CI](https://github.com/asad110abbas/streamlit-kpi-dashboard/actions/workflows/ci.yml/badge.svg)

> ⚡ **BRIHA: The Genesis of AGI.** This is a **Briha Data Lab** module, part of the [BRIHA AI World](https://github.com/asad110abbas), built by **Syed Asad Abbas**.

An interactive web dashboard for sales performance, built with **Streamlit** and **Plotly**. Filter by date range,
region, product line and channel, and every KPI and chart updates instantly, with **period-over-period deltas**.

## Features
- KPI cards (Revenue, Orders, AOV, Gross Margin) with change vs. the previous equal-length period
- Weekly revenue trend by channel, product-mix donut, region bar colored by margin
- Sortable product-line table with margin and share
- One-click CSV export of the filtered data
- KPI logic kept in pure functions (`dashboard/kpis.py`) and unit-tested, separate from the UI

## Run
```bash
pip install -r requirements.txt
streamlit run app.py          # http://localhost:8501
pytest -q
```
Deploy for free on Streamlit Community Cloud by pointing it at `app.py`.

## Structure
```
app.py               Streamlit UI
dashboard/data.py    synthetic sales generator (seasonality, channel growth)
dashboard/kpis.py    KPI calculations (tested)
tests/               pytest suite
```

> The data is synthetic.
