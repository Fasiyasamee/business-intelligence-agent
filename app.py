
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from ai_assistant import answer_question

st.set_page_config(
    page_title="Business Intelligence Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Intelligence Agent")
st.write("AI-powered business analytics and decision support.")

# -----------------------------------
# 1. DATA UPLOAD
# -----------------------------------

st.sidebar.header("📂 Business Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload your sales CSV",
    type=["csv"]
)

required_columns = [
    "Order_ID", "Date", "Product", "Category",
    "Quantity", "Unit_Price", "Cost"
]

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("Uploaded dataset selected!")
    except Exception as e:
        st.error(f"Could not read CSV: {e}")
        st.stop()
else:
    df = pd.read_csv("sales_data.csv")
    st.sidebar.info("Using sample dataset.")

missing = [c for c in required_columns if c not in df.columns]

if missing:
    st.error("Missing required columns: " + ", ".join(missing))
    st.stop()

if df.empty:
    st.error("The dataset is empty.")
    st.stop()

for col in ["Quantity", "Unit_Price", "Cost"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

if df[["Quantity", "Unit_Price", "Cost"]].isna().any().any():
    st.error("Please fix missing or invalid quantity, price or cost values.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -----------------------------------
# 2. CALCULATIONS
# -----------------------------------

df["Revenue"] = df["Quantity"] * df["Unit_Price"]
df["Profit"] = df["Quantity"] * (df["Unit_Price"] - df["Cost"])

# -----------------------------------
# 3. FILTERS
# -----------------------------------

st.sidebar.header("Dashboard Filters")

categories = sorted(df["Category"].dropna().unique())
products = sorted(df["Product"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select Categories",
    categories,
    default=categories
)

selected_products = st.sidebar.multiselect(
    "Select Products",
    products,
    default=products
)

filtered_df = df[
    (df["Category"].isin(selected_categories)) &
    (df["Product"].isin(selected_products))
].copy()

if filtered_df.empty:
    st.warning("No records match your filters.")
    st.stop()

# -----------------------------------
# 4. DASHBOARD METRICS
# -----------------------------------

total_revenue = filtered_df["Revenue"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)

product_profit = filtered_df.groupby("Product")["Profit"].sum()
category_revenue = filtered_df.groupby("Category")["Revenue"].sum()

best_product = product_profit.idxmax()
worst_product = product_profit.idxmin()

st.subheader("Business Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Revenue", f"{total_revenue:,.2f}")
c2.metric("Total Profit", f"{total_profit:,.2f}")
c3.metric("Total Orders", f"{total_orders:,}")
c4.metric("Top Product", str(best_product))

# -----------------------------------
# 5. CHARTS
# -----------------------------------

st.subheader("Product Profit Analysis")

fig1, ax1 = plt.subplots()
product_profit.sort_values().plot(kind="barh", ax=ax1)
ax1.set_xlabel("Profit")
ax1.set_ylabel("Product")
st.pyplot(fig1)
plt.close(fig1)

st.subheader("Category Revenue Analysis")

fig2, ax2 = plt.subplots()
category_revenue.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Revenue")
ax2.set_xlabel("Category")
st.pyplot(fig2)
plt.close(fig2)

# -----------------------------------
# 6. MONTHLY ANALYSIS
# -----------------------------------

st.subheader("Monthly Performance")

monthly_df = filtered_df.dropna(subset=["Date"]).copy()

if not monthly_df.empty:
    monthly_df["Month"] = monthly_df["Date"].dt.to_period("M").astype(str)

    monthly_summary = monthly_df.groupby("Month")[
        ["Revenue", "Profit"]
    ].sum()

    st.line_chart(monthly_summary)
else:
    st.info("No valid dates available for monthly analysis.")

# -----------------------------------
# 7. BUSINESS INSIGHTS
# -----------------------------------

st.subheader("💡 Business Insights")

st.write(f"Total revenue generated: **{total_revenue:,.2f}**")
st.write(f"Total profit generated: **{total_profit:,.2f}**")
st.write(f"Most profitable product: **{best_product}**")
st.write(f"Least profitable product: **{worst_product}**")

st.write("Revenue by category:")

for category, revenue in category_revenue.items():
    st.write(f"- {category}: {revenue:,.2f}")

# -----------------------------------
# 8. RAW DATA
# -----------------------------------

with st.expander("View Business Data"):
    st.dataframe(filtered_df, use_container_width=True)

# -----------------------------------
# 9. EXCEL DOWNLOAD
# -----------------------------------

st.subheader("📥 Download Reports")

excel_buffer = BytesIO()

with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    filtered_df.to_excel(writer, index=False, sheet_name="Sales Data")
    product_profit.to_frame("Profit").to_excel(
        writer, sheet_name="Product Analysis"
    )
    category_revenue.to_frame("Revenue").to_excel(
        writer, sheet_name="Category Analysis"
    )

st.download_button(
    "Download Excel Report",
    data=excel_buffer.getvalue(),
    file_name="business_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# -----------------------------------
# 10. PDF DOWNLOAD
# -----------------------------------

pdf_buffer = BytesIO()
pdf = canvas.Canvas(pdf_buffer)

pdf.setFont("Helvetica-Bold", 18)
pdf.drawString(50, 790, "Business Intelligence Report")

pdf.setFont("Helvetica", 11)
pdf.drawString(50, 745, f"Total Revenue: {total_revenue:,.2f}")
pdf.drawString(50, 720, f"Total Profit: {total_profit:,.2f}")
pdf.drawString(50, 695, f"Total Orders: {total_orders}")
pdf.drawString(50, 670, f"Top Product: {best_product}")
pdf.drawString(50, 645, f"Weakest Product: {worst_product}")

pdf.drawString(50, 605, "Category Revenue:")

y = 580
for category, revenue in category_revenue.items():
    pdf.drawString(60, y, f"{category}: {revenue:,.2f}")
    y -= 20

pdf.save()

st.download_button(
    "Download PDF Report",
    data=pdf_buffer.getvalue(),
    file_name="business_report.pdf",
    mime="application/pdf"
)

# -----------------------------------
# 11. AI BUSINESS ASSISTANT
# -----------------------------------

st.divider()
st.header("🤖 AI Business Assistant")

st.write("Ask questions about your business data.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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
        with st.spinner("Analysing your business..."):

            try:
                previous_messages = st.session_state.chat_history[-8:]

                conversation = "\n".join(
                    f'{msg["role"]}: {msg["content"]}'
                    for msg in previous_messages
                )

                answer = answer_question(conversation, filtered_df)

                st.markdown(answer)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"AI Assistant error: {e}")

if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

st.caption("Business Intelligence Agent | Python + Streamlit + Ollama")

