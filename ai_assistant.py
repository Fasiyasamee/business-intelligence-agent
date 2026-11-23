
import pandas as pd
import ollama


def answer_question(question, df):

    data = df.copy()

    # Calculate revenue and profit
    data["Revenue"] = data["Quantity"] * data["Unit_Price"]
    data["Profit"] = data["Quantity"] * (
        data["Unit_Price"] - data["Cost"]
    )

    # Overall business performance
    total_revenue = data["Revenue"].sum()
    total_profit = data["Profit"].sum()
    total_orders = len(data)

    # Product performance
    product_summary = data.groupby("Product").agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Quantity_Sold=("Quantity", "sum")
    ).sort_values("Profit", ascending=False)

    # Category performance
    category_summary = data.groupby("Category").agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Quantity_Sold=("Quantity", "sum")
    ).sort_values("Revenue", ascending=False)

    # Monthly trends
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

    valid_dates = data.dropna(subset=["Date"])

    if not valid_dates.empty:
        monthly_summary = valid_dates.groupby(
            valid_dates["Date"].dt.to_period("M")
        ).agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum")
        )
        monthly_summary.index = monthly_summary.index.astype(str)
        monthly_data = monthly_summary.to_string()
    else:
        monthly_data = "Monthly trend data is unavailable."

    # Identify strongest and weakest products
    best_product = product_summary["Profit"].idxmax()
    worst_product = product_summary["Profit"].idxmin()

    # Give the AI the actual business information
    business_data = f"""
BUSINESS OVERVIEW

Total Revenue: {total_revenue}
Total Profit: {total_profit}
Total Orders: {total_orders}

PRODUCT PERFORMANCE:
{product_summary.to_string()}

CATEGORY PERFORMANCE:
{category_summary.to_string()}

MONTHLY PERFORMANCE:
{monthly_data}

Most Profitable Product: {best_product}
Least Profitable Product: {worst_product}
"""

    prompt = f"""
You are an advanced Business Intelligence Analyst.

Analyse the business data and answer the user's question.

You can help with:
- Revenue and profit analysis
- Product comparisons
- Category comparisons
- Monthly performance trends
- Identifying weak-performing products
- Business opportunities
- Practical recommendations

IMPORTANT RULES:
1. Use the supplied business data.
2. Never invent numbers or trends.
3. Explain calculations and comparisons clearly.
4. Use simple, professional language.
5. Give actionable recommendations.
6. If information is unavailable, say so.
7. Format answers with headings and bullet points when useful.

BUSINESS DATA:
{business_data}

USER QUESTION:
{question}
"""

    response = ollama.chat(
        model="llama3.2:1b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# Terminal chatbot
# This does not run when Streamlit imports this file.

if __name__ == "__main__":

    df = pd.read_csv("sales_data.csv")

    print("\nAI BUSINESS INTELLIGENCE 2.0")
    print("Ask a business question or type 'exit'.\n")

    while True:

        question = input("You: ")

        if question.lower().strip() == "exit":
            print("Goodbye!")
            break

        try:
            answer = answer_question(question, df)
            print("\nAI Assistant:", answer, "\n")

        except Exception as e:
            print("\nSomething went wrong:", e)
