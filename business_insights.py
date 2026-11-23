
import pandas as pd

# Load sales data
df = pd.read_csv("sales_data.csv")

# Calculate revenue and profit
df["Revenue"] = df["Quantity"] * df["Unit_Price"]
df["Profit"] = df["Quantity"] * (
    df["Unit_Price"] - df["Cost"]
)

# Business insights
total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()

product_profit = df.groupby("Product")["Profit"].sum()
category_revenue = df.groupby("Category")["Revenue"].sum()

best_product = product_profit.idxmax()
worst_product = product_profit.idxmin()
best_category = category_revenue.idxmax()

# Display report
print("\n========== BUSINESS INTELLIGENCE REPORT ==========")

print(f"\nTotal Revenue: {total_revenue:.2f}")
print(f"Total Profit: {total_profit:.2f}")

print(f"\nMost Profitable Product: {best_product}")
print(f"Least Profitable Product: {worst_product}")
print(f"Highest Revenue Category: {best_category}")

print("\n========== PRODUCT PROFIT ANALYSIS ==========")
print(product_profit)

print("\n========== CATEGORY REVENUE ANALYSIS ==========")
print(category_revenue)

print("\n========== BUSINESS RECOMMENDATION ==========")
print(f"Focus on promoting {best_product}.")
print(f"Investigate the performance of {worst_product}.")

print("\nReport generated successfully!")
