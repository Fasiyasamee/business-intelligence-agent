
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from ai_assistant import answer_question

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Business Intelligence Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Intelligence Agent")
st.caption("AI-powered business analytics and decision support")

# =====================================
# LOAD DATA
# =====================================

try:
    df = pd.read_csv("sales_data.csv")
except Exception as e:
    st.error(f"Could not load sales_data.csv: {e}")
    st.stop()

required_columns = [
    "Order_ID", "Date", "Product",
    "Category", "Quantity", "Unit_Price", "Cost"
]

if not all(column in df.columns for column in required_columns):
    st.error("Your CSV file is missing one or more required columns.")
    st.stop()

df["Revenue"] = df["Quantity"] * df["Unit_Price"]
df["Profit"] = df["Quantity"] * (df["Unit_Price"] - df["Cost"])

# =====================================
# DASHBOARD FILTERS
# =====================================

st.sidebar.header("Dashboard Filters")

categories = sorted(df["Category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select Categories",
    categories,
    default=categories
)

products = sorted(df["Product"].dropna().unique())

selected_products = st.sidebar.multiselect(
    "Select Products",
    products,
    default=products
)

df = df[
    (df["Category"].isin(selected_categories)) &
    (df["Product"].isin(selected_products))
].copy()

if df.empty:
    st.warning("No sales data matches your filters. Please select a category or product.")
    st.stop()

# =====================================
# KEY BUSINESS METRICS
# =====================================

total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
total_orders = len(df)

product_profit = df.groupby("Product")["Profit"].sum()
category_revenue = df.groupby("Category")["Revenue"].sum()

best_product = product_profit.idxmax()
worst_product = product_profit.idxmin()

# =====================================
# KPI CARDS
# =====================================

st.subheader("Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"{total_revenue:,.2f}")
col2.metric("Total Profit", f"{total_profit:,.2f}")
col3.metric("Total Orders", total_orders)
col4.metric("Top Product", best_product)

st.divider()

# =====================================
# PRODUCT PROFIT CHART
# =====================================

st.subheader("Product Profit Analysis")

fig1, ax1 = plt.subplots()

product_profit.plot(kind="bar", ax=ax1)

ax1.set_xlabel("Product")
ax1.set_ylabel("Profit")
ax1.set_title("Profit by Product")

plt.xticks(rotation=30, ha="right")
plt.tight_layout()

st.pyplot(fig1)
plt.close(fig1)

# =====================================
# CATEGORY REVENUE CHART
# =====================================

st.subheader("Category Revenue Analysis")

fig2, ax2 = plt.subplots()

category_revenue.plot(
    kind="bar",
    ax=ax2
)

ax2.set_xlabel("Category")
ax2.set_ylabel("Revenue")
ax2.set_title("Revenue by Category")

plt.xticks(rotation=30, ha="right")
plt.tight_layout()

st.pyplot(fig2)
plt.close(fig2)

# =====================================
# BUSINESS INSIGHTS
# =====================================

st.divider()
st.subheader("💡 Business Insights")

st.write(
    f"**Most profitable product:** {best_product}"
)

st.write(
    f"**Product requiring attention:** {worst_product}"
)

st.write(
    f"**Total business revenue:** {total_revenue:,.2f}"
)

st.write(
    f"**Total business profit:** {total_profit:,.2f}"
)

st.info(
    f"Recommendation: Focus on promoting {best_product} "
    f"and investigate the performance of {worst_product}."
)

# =====================================
# RAW SALES DATA
# =====================================

with st.expander("View Raw Sales Data"):
    st.dataframe(df, use_container_width=True)

# =====================================
# DOWNLOAD BUSINESS REPORTS
# =====================================

st.divider()
st.header("📥 Download Business Reports")

# Excel report

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:
    df.to_excel(
        writer,
        index=False,
        sheet_name="Sales Report"
    )

st.download_button(
    label="Download Excel Report",
    data=excel_buffer.getvalue(),
    file_name="business_sales_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# PDF report

pdf_buffer = BytesIO()

pdf = canvas.Canvas(
    pdf_buffer,
    pagesize=letter
)

pdf.drawString(50, 750, "BUSINESS INTELLIGENCE REPORT")
pdf.drawString(50, 710, f"Total Revenue: {total_revenue:,.2f}")
pdf.drawString(50, 680, f"Total Profit: {total_profit:,.2f}")
pdf.drawString(50, 650, f"Total Orders: {total_orders}")
pdf.drawString(50, 620, f"Most Profitable Product: {best_product}")
pdf.drawString(50, 590, f"Product Requiring Attention: {worst_product}")

pdf.drawString(50, 540, "Category Revenue Analysis:")

y = 510

for category, revenue in category_revenue.items():
    if y < 50:
        pdf.showPage()
        y = 750

    pdf.drawString(
        60,
        y,
        f"{category}: {revenue:,.2f}"
    )

    y -= 25

pdf.save()

st.download_button(
    label="Download PDF Report",
    data=pdf_buffer.getvalue(),
    file_name="business_management_report.pdf",
    mime="application/pdf"
)

# =====================================
# AI BUSINESS ASSISTANT
# =====================================

st.divider()

st.divider()
st.header("🤖 AI Business Assistant")
st.write("Ask questions and explore your business data.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

question = st.chat_input("Ask me anything about your business...")

if question:
    st.session_state.chat_history.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Include recent conversation in the question
                previous_messages = st.session_state.chat_history[-8:]

                conversation = "\n".join(
                    f'{msg["role"]}: {msg["content"]}'
                    for msg in previous_messages
                )

                answer = answer_question(conversation, df)

                st.markdown(answer)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")

if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
