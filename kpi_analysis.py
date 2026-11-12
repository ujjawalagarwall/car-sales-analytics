
import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/cleaned_car_sales.csv")

# ---------- Overall KPIs ----------

total_revenue = df["Price ($)"].sum()
total_units = df["Car_id"].nunique()
avg_price = total_revenue / total_units

print("========== OVERALL KPIs ==========")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Units Sold: {total_units:,}")
print(f"Average Selling Price: ${avg_price:,.2f}")

# ---------- Yearly Sales ----------

yearly = df.groupby("Year").agg(
    Revenue=("Price ($)", "sum"),
    Units_Sold=("Car_id", "nunique")
).sort_index()

yearly["Average_Price"] = (
    yearly["Revenue"] / yearly["Units_Sold"]
)

yearly["Revenue_Growth_%"] = (
    yearly["Revenue"].pct_change() * 100
)

yearly["Units_Growth_%"] = (
    yearly["Units_Sold"].pct_change() * 100
)

print("\n========== YEARLY PERFORMANCE ==========")
print(yearly.round(2).to_string())

# ---------- Company Performance ----------

company = df.groupby("Company").agg(
    Revenue=("Price ($)", "sum"),
    Units=("Car_id", "nunique")
)

company = company.sort_values(
    "Revenue", ascending=False
)

print("\n========== TOP 10 COMPANIES ==========")
print(company.head(10).to_string())

# ---------- Regional Performance ----------

region = df.groupby("Dealer_Region").agg(
    Revenue=("Price ($)", "sum"),
    Units=("Car_id", "nunique")
)

region = region.sort_values(
    "Revenue", ascending=False
)

print("\n========== REGIONAL PERFORMANCE ==========")
print(region.to_string())

# ---------- DATE COVERAGE ANALYSIS ----------

df["Date"] = pd.to_datetime(df["Date"])

print("\n========== DATE COVERAGE ==========")

for year, group in df.groupby("Year"):
    print(f"\nYear: {year}")
    print("First Sale:", group["Date"].min().date())
    print("Last Sale:", group["Date"].max().date())
    print("Transactions:", len(group))

print("\n========== MONTHLY SALES ==========")

monthly = df.groupby(
    ["Year", "Month"]
).agg(
    Revenue=("Price ($)", "sum"),
    Units=("Car_id", "nunique")
).reset_index()

print(monthly.to_string(index=False))

# Compare only months represented in both years
months_2022 = set(
    monthly.loc[monthly["Year"] == 2022, "Month"]
)

months_2023 = set(
    monthly.loc[monthly["Year"] == 2023, "Month"]
)

common_months = sorted(months_2022 & months_2023)

print("\nCommon Months:", common_months)

matched = monthly[
    monthly["Month"].isin(common_months)
].groupby("Year")[["Revenue", "Units"]].sum()

print("\n========== MATCHED-MONTH COMPARISON ==========")
print(matched)

if 2022 in matched.index and 2023 in matched.index:
    revenue_growth = (
        matched.loc[2023, "Revenue"]
        / matched.loc[2022, "Revenue"] - 1
    ) * 100

    units_growth = (
        matched.loc[2023, "Units"]
        / matched.loc[2022, "Units"] - 1
    ) * 100

    print(f"\nRevenue Growth: {revenue_growth:.2f}%")
    print(f"Units Growth: {units_growth:.2f}%")
