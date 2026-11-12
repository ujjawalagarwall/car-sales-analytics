
import pandas as pd

df = pd.read_csv("data/cleaned_car_sales.csv")

# 1. Manufacturer performance
company = df.groupby("Company").agg(
    Revenue=("Price ($)", "sum"),
    Units=("Car_id", "nunique"),
    Avg_Price=("Price ($)", "mean")
)

company["Revenue_Share_%"] = (
    company["Revenue"] / df["Price ($)"].sum() * 100
)

print("\n========== TOP MANUFACTURERS ==========")
print(
    company.sort_values("Revenue", ascending=False)
    .head(10).round(2).to_string()
)

# 2. Body-style performance
body = df.groupby("Body Style").agg(
    Revenue=("Price ($)", "sum"),
    Units=("Car_id", "nunique"),
    Avg_Price=("Price ($)", "mean")
)

print("\n========== BODY STYLE PERFORMANCE ==========")
print(body.sort_values("Revenue", ascending=False).round(2))

# 3. Regional average selling price
region = df.groupby("Dealer_Region").agg(
    Revenue=("Price ($)", "sum"),
    Units=("Car_id", "nunique"),
    Avg_Price=("Price ($)", "mean")
)

print("\n========== REGIONAL PERFORMANCE ==========")
print(region.sort_values("Revenue", ascending=False).round(2))

# 4. Customer income segments
df["Income_Segment"] = pd.cut(
    df["Annual Income"],
    bins=[float("-inf"), 50000, 100000, 150000, float("inf")],
    labels=["Low", "Medium", "High", "Premium"]
)

income = df.groupby(
    "Income_Segment", observed=True
).agg(
    Customers=("Car_id", "nunique"),
    Avg_Car_Price=("Price ($)", "mean")
)

print("\n========== INCOME SEGMENTS ==========")
print(income.round(2))

# 5. Top selling models
models = df.groupby(["Company", "Model"]).agg(
    Revenue=("Price ($)", "sum"),
    Units=("Car_id", "nunique")
)

print("\n========== TOP 10 MODELS ==========")
print(
    models.sort_values("Revenue", ascending=False)
    .head(10).to_string()
)

# ---------- INCOME DATA QUALITY CHECKS ----------

print("\n========== INCOME DISTRIBUTION ==========")

print(
    df["Annual Income"].describe(
        percentiles=[0.01, 0.25, 0.50, 0.75, 0.99]
    )
)

print("\n========== LOWEST 10 INCOMES ==========")
print(df["Annual Income"].nsmallest(10).to_string(index=False))

print("\n========== HIGHEST 10 INCOMES ==========")
print(df["Annual Income"].nlargest(10).to_string(index=False))

print("\n========== INCOME QUALITY CHECKS ==========")
print("Missing incomes:", df["Annual Income"].isna().sum())
print("Zero incomes:", (df["Annual Income"] == 0).sum())
print("Negative incomes:", (df["Annual Income"] < 0).sum())

# ---------- CUSTOMER UNIQUENESS ----------

print("\n========== CUSTOMER ANALYSIS ==========")

print("Total transactions:", len(df))
print("Unique customer names:", df["Customer Name"].nunique())

print("\nMost frequent customer names:")
print(df["Customer Name"].value_counts().head(10))

# ---------- QUANTILE INCOME SEGMENTATION ----------

df["Income_Quartile"] = pd.qcut(
    df["Annual Income"],
    q=4,
    labels=["Q1", "Q2", "Q3", "Q4"],
    duplicates="raise"
)

quartile_analysis = df.groupby(
    "Income_Quartile",
    observed=True
).agg(
    Transactions=("Car_id", "nunique"),
    Avg_Income=("Annual Income", "mean"),
    Avg_Car_Price=("Price ($)", "mean"),
    Revenue=("Price ($)", "sum")
)

print("\n========== QUARTILE SEGMENTATION ==========")
print(quartile_analysis.round(2).to_string())
