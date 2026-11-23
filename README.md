
# Business Intelligence Agent

An AI-powered Business Intelligence application that analyses sales data, generates business insights, and answers questions using a local AI model.

## Features

- Interactive business dashboard
- Revenue and profit calculations
- Product and category performance analysis
- Monthly business performance analysis
- Interactive charts and visualisations
- Excel and PDF report downloads
- AI-powered business assistant
- Conversational chat history

## Technologies Used

- Python 3.12
- Pandas
- Streamlit
- Matplotlib
- Ollama
- Llama 3.2 (1B)

## Project Structure

- app.py – Main Streamlit dashboard
- ai_assistant.py – AI business assistant
- sales_data.csv – Sample sales dataset
- visual_analysis.py – Data visualisation
- business_insights.py – Business insights

## How to Run

1. Install Python and the required packages.
2. Install Ollama and download the model:

   ollama pull llama3.2:1b

3. Open the project folder in the terminal.
4. Run:

   py -3.12 -m streamlit run app.py

## Purpose

This project demonstrates how Python, data analytics, dashboards, and local AI models can work together to support business decision-making.
