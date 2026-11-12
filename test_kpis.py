
import pandas as pd

df = pd.read_csv("data/cleaned_car_sales.csv")

# Test 1: Transaction IDs should be unique
assert df["Car_id"].is_unique, "Duplicate transaction IDs found"

# Test 2: No missing transaction IDs
assert df["Car_id"].notna().all(), "Missing transaction IDs found"

# Test 3: No missing or negative prices
assert df["Price ($)"].notna().all(), "Missing prices found"
assert (df["Price ($)"] >= 0).all(), "Negative prices found"

# Test 4: Revenue should equal sum of yearly revenue
total_revenue = df["Price ($)"].sum()
yearly_revenue = df.groupby("Year")["Price ($)"].sum().sum()

assert total_revenue == yearly_revenue, "Revenue mismatch"

# Test 5: Units should equal sum of yearly units
total_units = df["Car_id"].nunique()
yearly_units = df.groupby("Year")["Car_id"].nunique().sum()

assert total_units == yearly_units, "Unit count mismatch"

# Test 6: Verify average selling price
average_price = total_revenue / total_units

assert abs(
    average_price - df["Price ($)"].mean()
) < 0.01, "Average price mismatch"

print("All 6 KPI validation checks passed!")
