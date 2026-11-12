
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="US Car Sales Analytics",
    page_icon="🚗",
    layout="wide"
)

@st.cache_data
def load_data():
    data = pd.read_csv(
        "data/cleaned_car_sales.csv",
        parse_dates=["Date"]
    )
    return data

df = load_data()

st.title("🚗 US Car Sales Analytics")
st.caption("Executive sales intelligence | 2022–2023")

# ---------- SIDEBAR FILTERS ----------

st.sidebar.header("Filters")

years = sorted(df["Year"].unique())
companies = sorted(df["Company"].unique())
regions = sorted(df["Dealer_Region"].unique())

selected_years = st.sidebar.multiselect(
    "Year", years, default=years
)

selected_companies = st.sidebar.multiselect(
    "Manufacturer", companies, default=companies
)

selected_regions = st.sidebar.multiselect(
    "Dealer Region", regions, default=regions
)

filtered = df[
    df["Year"].isin(selected_years)
    & df["Company"].isin(selected_companies)
    & df["Dealer_Region"].isin(selected_regions)
].copy()

if filtered.empty:
    st.warning("No records match these filters.")
    st.stop()

# ---------- KPI CARDS ----------

revenue = filtered["Price ($)"].sum()
units = filtered["Car_id"].nunique()
avg_price = revenue / units

c1, c2, c3 = st.columns(3)

c1.metric("Total Revenue", f"${revenue/1e6:,.2f}M")
c2.metric("Units Sold", f"{units:,}")
c3.metric("Average Selling Price", f"${avg_price:,.0f}")

# ---------- DASHBOARD TABS ----------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Overview",
    "Sales Trends",
    "Manufacturers",
    "Regions",
    "Customer Segments"
])

# ---------- EXECUTIVE OVERVIEW ----------

with tab1:
    st.subheader("Executive Overview")

    yearly = filtered.groupby("Year").agg(
        Revenue=("Price ($)", "sum"),
        Units=("Car_id", "nunique")
    ).sort_index()

    yearly["Revenue Growth (%)"] = (
        yearly["Revenue"].pct_change() * 100
    )

    yearly["Units Growth (%)"] = (
        yearly["Units"].pct_change() * 100
    )

    st.dataframe(yearly.round(2), use_container_width=True)

    top_company = (
        filtered.groupby("Company")["Price ($)"]
        .sum().idxmax()
    )

    top_region = (
        filtered.groupby("Dealer_Region")["Price ($)"]
        .sum().idxmax()
    )

    top_style = (
        filtered.groupby("Body Style")["Car_id"]
        .nunique().idxmax()
    )

    st.markdown("### Key Findings")
    st.write(f"Leading manufacturer: **{top_company}**")
    st.write(f"Highest-revenue region: **{top_region}**")
    st.write(f"Most popular body style: **{top_style}**")

    st.info(
        "Sales performance is descriptive. "
        "Profitability requires additional cost and margin data."
    )

# ---------- SALES TRENDS ----------

with tab2:
    st.subheader("Monthly Revenue Trend")

    monthly = (
        filtered.groupby(
            pd.Grouper(key="Date", freq="MS")
        )["Price ($)"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="Date",
        y="Price ($)",
        markers=True,
        title="Monthly Sales Revenue"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Quarterly Revenue")

    quarterly = (
        filtered.groupby(["Year", "Quarter"])["Price ($)"]
        .sum()
        .reset_index()
    )

    quarterly["Period"] = (
        quarterly["Year"].astype(str)
        + "-Q"
        + quarterly["Quarter"].astype(str)
    )

    fig = px.bar(
        quarterly,
        x="Period",
        y="Price ($)",
        title="Quarterly Sales Performance"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------- MANUFACTURER ANALYSIS ----------

with tab3:
    st.subheader("Manufacturer Performance")

    manufacturer = filtered.groupby("Company").agg(
        Revenue=("Price ($)", "sum"),
        Units=("Car_id", "nunique")
    ).reset_index()

    manufacturer["Average Price"] = (
        manufacturer["Revenue"] / manufacturer["Units"]
    )

    manufacturer["Revenue Share (%)"] = (
        manufacturer["Revenue"] / revenue * 100
    )

    manufacturer = manufacturer.sort_values(
        "Revenue", ascending=False
    )

    fig = px.bar(
        manufacturer.head(10),
        x="Company",
        y="Revenue",
        title="Top 10 Manufacturers by Revenue"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(manufacturer, use_container_width=True)

# ---------- REGIONAL ANALYSIS ----------

with tab4:
    st.subheader("Dealer Region Performance")

    regional = filtered.groupby("Dealer_Region").agg(
        Revenue=("Price ($)", "sum"),
        Units=("Car_id", "nunique")
    ).reset_index()

    regional["Average Price"] = (
        regional["Revenue"] / regional["Units"]
    )

    regional = regional.sort_values(
        "Revenue", ascending=False
    )

    fig = px.bar(
        regional,
        x="Dealer_Region",
        y="Revenue",
        title="Revenue by Dealer Region"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(regional, use_container_width=True)

# ---------- CUSTOMER SEGMENTATION ----------

with tab5:
    st.subheader("Income Quartile Analysis")

    st.caption(
        "Quartiles are calculated from the complete dataset "
        "and then filtered for comparison."
    )

    # Assign income quartiles using all records
    full_df = df.copy()

    full_df["Income_Quartile"] = pd.qcut(
        full_df["Annual Income"],
        q=4,
        labels=["Q1", "Q2", "Q3", "Q4"]
    )

    selected_ids = set(filtered["Car_id"])

    segment_data = full_df[
        full_df["Car_id"].isin(selected_ids)
    ]

    segments = segment_data.groupby(
        "Income_Quartile",
        observed=True
    ).agg(
        Transactions=("Car_id", "nunique"),
        Avg_Car_Price=("Price ($)", "mean")
    ).reset_index()

    fig = px.bar(
        segments,
        x="Income_Quartile",
        y="Avg_Car_Price",
        title="Average Car Price by Income Quartile"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(segments, use_container_width=True)

    st.warning(
        "Customer names are not unique identifiers. "
        "Income values are unusually high and should "
        "be interpreted cautiously."
    )

# ---------- DOWNLOAD ----------

st.divider()

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Sales Data",
    data=csv,
    file_name="filtered_car_sales.csv",
    mime="text/csv"
)
