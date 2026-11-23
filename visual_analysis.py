
import pandas as pd
import matplotlib.pyplot as plt

# Load our sales data
df = pd.read_csv("sales_data.csv")

# Calculate revenue and profit
df["Revenue"] = df["Quantity"] * df["Unit_Price"]
df["Profit"] = df["Revenue"] - (df["Quantity"] * df["Cost"])

# Calculate profit by product
product_profit = df.groupby("Product")["Profit"].sum()

# Create a bar chart
product_profit.plot(kind="bar", color="skyblue")

plt.title("Profit by Product")
plt.xlabel("Product")
plt.ylabel("Total Profit")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("profit_chart.png")
plt.show()

print("Chart generated successfully!")
