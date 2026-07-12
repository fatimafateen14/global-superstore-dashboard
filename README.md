# Global Superstore Business Dashboard

An interactive Streamlit dashboard for analyzing sales, profit, and segment-wise performance across the Global Superstore dataset with live filtering by Region, Category, and Sub-Category.

**Live App:** (https://global-superstore-dashboard-nxn4ylemkjkwdv8xyeyb82.streamlit.app/)

## Problem Statement

Raw sales data is only useful if the people who need it managers, analysts, stakeholders can explore it themselves, without writing code. This project turns a static Superstore sales dataset into an interactive dashboard where key business metrics update live as filters change, making the data usable for non-technical decision-making.

## Dataset

**Global Superstore Dataset** ([Kaggle](https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset))

- Order-level retail transaction data across multiple countries and markets
- Key columns used: `Sales`, `Profit`, `Region`, `Category`, `Sub-Category`, `Customer Name`, `Order Date`

## Features

- **Sidebar filters** — Region, Category, and Sub-Category (Sub-Category options dynamically narrow based on selected Category)
- **KPI cards** — Total Sales, Total Profit, Profit Margin, Total Orders
- **Sales & Profit by Category** — bar charts
- **Sales Distribution by Region** — pie chart
- **Profit by Sub-Category** — horizontal bar chart, color-coded by profitability
- **Top 5 Customers by Sales** — bar chart and table
- **Monthly Sales Trend** — line chart over time
- **Raw data explorer** — expandable table showing the currently filtered dataset

## Methodology

### 1. Data Cleaning
- Loaded raw CSV with `latin1` encoding (required due to special characters in product/customer names)
- Converted `Order Date` to datetime
- Coerced `Sales` and `Profit` to numeric, dropping rows with missing critical values
- Column-name auto-detection to handle minor naming variants across dataset re-uploads

### 2. Interactivity
- Built with Streamlit's `multiselect` widgets for filtering
- All KPIs and charts recalculate live based on the current filter selection using cached data loading (`st.cache_data`) for performance

### 3. Visualization
- Built with Plotly for interactive, hoverable charts (zoom, tooltips) rather than static Matplotlib images

## Tech Stack

- Python, Pandas
- Streamlit
- Plotly Express
- Deployed on Streamlit Community Cloud

## How to Run

### Option 1 — Live App
Visit the deployed link above.

### Option 2 — Run Locally
```bash
git clone https://github.com/fatimafateen14/global-superstore-dashboard.git
cd global-superstore-dashboard
pip install -r requirements.txt
streamlit run app.py
```

Make sure `superstore.csv` is in the same folder as `app.py`.

## Key Takeaways

- Demonstrates BI dashboarding: translating raw transactional data into an interactive decision-support tool
- Shows data storytelling through KPI framing and visual hierarchy (summary numbers → category breakdowns → customer-level detail)
- Practical use of Streamlit's reactive filtering model for real-time user interactivity

## Author

Fateen Fatima
[GitHub](https://github.com/fatimafateen14) | [LinkedIn](https://linkedin.com/in/fateen-fatima-213103322)
