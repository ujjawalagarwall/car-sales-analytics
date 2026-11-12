
# US Car Sales Analytics Dashboard

## Project Overview
An interactive sales analytics dashboard built using Python,
Pandas, SQLite, Streamlit, and Plotly.

The project analyzes 23,906 car sales transactions from 2022
and 2023 to identify sales trends, manufacturer performance,
regional patterns, and business insights.

## Tech Stack
- Python
- Pandas
- SQLite
- Streamlit
- Plotly

## Key Features
- Interactive five-tab dashboard
- Revenue, units sold, and average selling price KPIs
- Yearly and quarterly revenue analysis
- Manufacturer and regional performance comparisons
- Income quartile analysis
- Downloadable filtered sales data
- SQL-based KPI validation

## Verified Results
- Total Revenue: $671.53 million
- Total Cars Sold: 23,906
- Average Selling Price: $28,090
- 2023 Revenue Growth: 23.59%
- 2023 Unit Sales Growth: 24.57%

## How to Run

1. Create and activate a Python virtual environment.
2. Install dependencies:

   pip install -r requirements.txt

3. Place Car_Sales_dataset.csv in the data folder.
4. Run analysis.py to create cleaned_car_sales.csv.
5. Launch the dashboard:

   streamlit run app.py

## Data Limitations
- Customer names are not reliable unique identifiers.
- Income values are unusually high and require caution.
- Revenue metrics cannot establish profitability without
  cost and margin information.
- Growth rates may depend on the reporting period selected.
