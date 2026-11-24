
import os
import pandas as pd


def get_groq_api_key():
    # First check environment variables
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        return api_key

    # Then check Streamlit Cloud Secrets
    try:
        import streamlit as st
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return None


def answer_question(question, df):

    try:
        # Prepare sales data
        data = df.copy()

        if "Revenue" not in data.columns:
            data["Revenue"] = (
                data["Quantity"] * data["Unit_Price"]
            )

        if "Profit" not in data.columns:
            data["Profit"] = (
                data["Revenue"] - data["Cost"] * data["Quantity"]
            )

        total_revenue = data["Revenue"].sum()
        total_profit = data["Profit"].sum()
        total_orders = len(data)

        product_performance = (
            data.groupby("Product")[["Revenue", "Profit"]]
            .sum()
            .sort_values("Profit", ascending=False)
        )

        category_performance = (
            data.groupby("Category")[["Revenue", "Profit"]]
            .sum()
        )

        business_data = f"""
        TOTAL REVENUE: {total_revenue}
        TOTAL PROFIT: {total_profit}
        TOTAL ORDERS: {total_orders}

        PRODUCT PERFORMANCE:
        {product_performance.to_string()}

        CATEGORY PERFORMANCE:
        {category_performance.to_string()}
        """

        prompt = f"""
        You are an intelligent Business Intelligence Assistant.

        You help business owners understand their sales data.

        Use ONLY the business data provided below.
        Do not invent numbers or facts.
        If the data does not answer a question, say so.

        Give clear, useful business explanations.
        Use simple language and provide recommendations
        when appropriate.

        BUSINESS DATA:
        {business_data}

        USER QUESTION:
        {question}
        """

        api_key = get_groq_api_key()

        # Use Groq for the online app
        if api_key:
            from groq import Groq

            client = Groq(api_key=api_key)

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_completion_tokens=1200
            )

            return response.choices[0].message.content

        # Use local Ollama if no Groq key is configured
        import ollama

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

    except Exception as e:
        return f"AI Assistant Error: {str(e)}"


if __name__ == "__main__":

    df = pd.read_csv("sales_data.csv")

    print("Business Intelligence AI Assistant")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk a business question: ")

        if question.lower() == "exit":
            break

        print("\nAI:", answer_question(question, df))
