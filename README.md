# smart-store-foster-1
# 📈 Sales Growth Over Time – OLAP Analysis

## 🎯 Project Goal

**How is sales revenue changing over time, and are there any seasonal or monthly patterns we can identify?**

This analysis focuses on identifying sales growth trends, seasonal spikes, and product/region-specific performance using both Power BI and Python.

---

## 🧰 Tools Used

- **Power BI** – for drag-and-drop OLAP visualizations, slicing, dicing, and drilldowns
- **Python (Pandas, Seaborn, Matplotlib)** – for scripted visualizations, transformations, and deeper validation
- **SQLite** – data warehouse backend for storing sales data
- **Jupyter Notebooks / VS Code** – to write and test Python queries and visuals

---

## 📦 Data Overview

Tables used:
- `sale` – Sales data (amounts, dates, product/customer IDs)
- `customer` – Customer information including region
- `product` – Product details including category

Note: ProductID in the `sale` table had an offset of +100, which we adjusted to join correctly with the `product` table.

---

## 🔍 Step-by-Step Process

### 1. Prepare the Data

```python
import pandas as pd
import sqlite3

conn = sqlite3.connect('../data/dw/smart_sales.db')

df = pd.read_sql_query("""
SELECT 
    s.SaleAmount, 
    s.SaleDate, 
    c.Region, 
    p.Category,
    c.Name AS CustomerName,
    s.PaymentType
FROM sale s
LEFT JOIN customer c ON s.CustomerID = c.CustomerID
LEFT JOIN product p ON (s.ProductID - 100) = p.ProductID
""", conn)
We also extracted:

Year

Month Name

Quarter

From the SaleDate column:

python
Copy code
df['SaleDate'] = pd.to_datetime(df['SaleDate'])
df['Year'] = df['SaleDate'].dt.year
df['Month Name'] = df['SaleDate'].dt.strftime('%B')
df['Quarter'] = df['SaleDate'].dt.to_period("Q").astype(str)
2. Filter for 2024 Data
python
Copy code
df_2024 = df[df['Year'] == 2024].copy()
3. Perform OLAP Analysis
✅ Slicing – Sales by Product Category (2024)
python
Copy code
category_sales = df_2024.groupby('Category')['SaleAmount'].sum().reset_index()

sns.barplot(data=category_sales, x='Category', y='SaleAmount')
plt.title('Total Sales by Product Category (2024)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
✅ Dicing – Sales by Region per Month (2024)
python
Copy code
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
df_2024['Month Name'] = pd.Categorical(df_2024['Month Name'], categories=month_order, ordered=True)

monthly_region_sales = df_2024.groupby(['Region', 'Month Name'])['SaleAmount'].sum().reset_index()

sns.lineplot(data=monthly_region_sales, x='Month Name', y='SaleAmount', hue='Region', marker='o')
plt.title('Monthly Sales by Region (2024)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
✅ Drilldown – Monthly Sales % Growth by Region
python
Copy code
monthly_region_sales.sort_values(['Region', 'Month Name'], inplace=True)
monthly_region_sales['% Growth'] = monthly_region_sales.groupby('Region')['SaleAmount'].pct_change() * 100
monthly_region_sales['% Growth'] = monthly_region_sales['% Growth'].round(2)

sns.lineplot(data=monthly_region_sales, x='Month Name', y='% Growth', hue='Region', marker='o')
plt.title('Month-over-Month % Sales Growth by Region (2024)')
plt.axhline(0, color='gray', linestyle='--')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
✅ Business Questions Answered
Which regions show the most consistent sales growth year over year?

Identified via region-wise % growth charts

Do certain product categories drive most of the growth?

Bar charts showed top-selling categories in 2024

Are there seasonal spikes in sales (e.g., Q4)?

Monthly trends and quarter comparisons revealed strong Q4 trends

What months had the highest/lowest sales in 2024?

Clear peak and dip months shown through line and bar plots

🧪 Testing and Validation
Totals in Python matched Power BI’s aggregated views

OLAP queries were verified using slicing/dicing combinations

SaleAmount trends validated across time, region, and category

📊 Final Output
Power BI dashboards

Jupyter Notebook visualizations

Clean SQLite join and date-derived dimensions

🙌 Summary
This analysis provided strong insight into sales trends over time, helped detect seasonality, and revealed growth drivers by region and product — all critical for better business forecasting and planning.
