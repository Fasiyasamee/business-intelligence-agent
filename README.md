# Business Intelligence Agent

An AI-powered Business Intelligence Dashboard built using Python, Streamlit, Pandas, Matplotlib and Groq.

## Project Overview

The Business Intelligence Agent is a web-based application designed to help businesses understand their sales performance through interactive dashboards, data visualisations, automated business insights and an AI-powered assistant.

Users can explore sales data, analyse revenue and profit, compare product and category performance, and ask questions about their business data in natural language.

## Key Features

- **Sales Dashboard:** Displays important business metrics, including total revenue, profit, orders and top-performing products.
- **Data Visualisation:** Presents product profitability, category revenue and monthly performance through charts.
- **Business Insights:** Generates useful observations and recommendations from sales data.
- **AI Business Assistant:** Allows users to ask questions about their sales data using natural language.
- **Data Upload:** Supports uploading sales CSV files with the required column structure.
- **Excel Export:** Exports sales and analysis data into an Excel workbook.
- **PDF Export:** Generates downloadable business reports.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application and dashboard |
| Pandas | Data processing and analysis |
| Matplotlib | Data visualisation |
| Groq API | Hosted AI assistant |
| Ollama | Local AI model support |
| ReportLab | PDF report generation |
| OpenPyXL | Excel file generation |

## How It Works

1. The application loads sales data from a CSV file.
2. Pandas processes the data and calculates revenue and profit.
3. The dashboard displays business metrics and visualisations.
4. The application generates business insights from the processed data.
5. The AI assistant uses the sales information to answer user questions.
6. Users can export reports in Excel and PDF formats.

## Dataset Structure

The application expects these columns in the sales CSV file:

- Order_ID
- Date
- Product
- Category
- Quantity
- Unit_Price
- Cost

## Deployment

The application is deployed using Streamlit Community Cloud and connected to GitHub.

The online AI assistant uses the Groq API. The API key is configured through Streamlit Secrets and should never be committed to the public repository.

## Project Objective

The objective of this project is to demonstrate how Python, data analytics, visualisation and AI can be combined to build a practical business intelligence solution.

## Author

Developed as a hands-on Business Intelligence and AI project.
