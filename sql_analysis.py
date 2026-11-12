
import pandas as pd
import sqlite3

# Load cleaned dataset
df = pd.read_csv("data/cleaned_car_sales.csv")

# Connect to SQLite database
conn = sqlite3.connect("car_sales.db")

# Create SQL table
df.to_sql(
    "car_sales",
    conn,
    if_exists="replace",
    index=False
)

print("Database created successfully!")


# Query 1: Top 5 manufacturers by revenue
query1 = """
SELECT
    Company,
    COUNT(DISTINCT Car_id) AS Units_Sold,
    SUM("Price ($)") AS Revenue
FROM car_sales
GROUP BY Company
ORDER BY Revenue DESC
LIMIT 5;
"""

# Query 2: Regional sales
query2 = """
SELECT
    Dealer_Region,
    COUNT(DISTINCT Car_id) AS Units_Sold,
    SUM("Price ($)") AS Revenue
FROM car_sales
GROUP BY Dealer_Region
ORDER BY Revenue DESC;
"""

# Query 3: Year-over-year growth
query3 = """
WITH yearly AS (
    SELECT
        Year,
        SUM("Price ($)") AS Revenue,
        COUNT(DISTINCT Car_id) AS Units
    FROM car_sales
    GROUP BY Year
)
SELECT
    curr.Year,
    curr.Revenue,
    curr.Units,
    ROUND(
        (curr.Revenue * 1.0 / prev.Revenue - 1) * 100,
        2
    ) AS Revenue_Growth_Pct,
    ROUND(
        (curr.Units * 1.0 / prev.Units - 1) * 100,
        2
    ) AS Units_Growth_Pct
FROM yearly curr
LEFT JOIN yearly prev
    ON curr.Year = prev.Year + 1
ORDER BY curr.Year;
"""

queries = {
    "TOP MANUFACTURERS": query1,
    "REGIONAL PERFORMANCE": query2,
    "YEARLY GROWTH": query3
}

for name, query in queries.items():
    print(f"\n========== {name} ==========")
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))

conn.close()


