
import pandas as pd
from pathlib import Path

Path("data").mkdir(exist_ok=True)
# 1. Load dataset
df = pd.read_csv("data/Car_Sales_dataset.csv")

print("Original Shape:", df.shape)

# 2. Clean column names
df.columns = df.columns.str.strip()

# 3. Handle missing customer names
df["Customer Name"] = df["Customer Name"].fillna("Unknown")

# 4. Convert Date into datetime
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%m/%d/%Y"
)

# 5. Remove duplicate transactions if any
df = df.drop_duplicates(subset=["Car_id"])

# 6. Create useful time features
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.month_name()
df["Quarter"] = df["Date"].dt.quarter

# 7. Verify the cleaned dataset
print("\nCleaned Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nData Types:")
print(df.dtypes)

print("\nDate Range:")
print(df["Date"].min(), "to", df["Date"].max())

# 8. Save cleaned dataset
df.to_csv("data/cleaned_car_sales.csv", index=False)

print("\nCleaned dataset saved successfully!")
