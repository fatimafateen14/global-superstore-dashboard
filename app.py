import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Page Config ----------
st.set_page_config(page_title="Global Superstore Dashboard", layout="wide")

# ---------- Helper: find a column regardless of exact naming ----------
def find_col(df, *candidates):
    for c in candidates:
        if c in df.columns:
            return c
    # fallback: case-insensitive, ignore spaces/hyphens
    normalized = {col.lower().replace(" ", "").replace("-", ""): col for col in df.columns}
    for c in candidates:
        key = c.lower().replace(" ", "").replace("-", "")
        if key in normalized:
            return normalized[key]
    return None

# ---------- Load & Clean Data ----------
@st.cache_data
def load_data():
    df = pd.read_csv("superstore.csv", encoding="latin1")
    df.columns = [c.strip() for c in df.columns]

    col_sales = find_col(df, "Sales")
    col_profit = find_col(df, "Profit")
    col_region = find_col(df, "Region")
    col_category = find_col(df, "Category")
    col_subcat = find_col(df, "Sub-Category", "Sub Category")
    col_customer = find_col(df, "Customer Name", "CustomerName")
    col_date = find_col(df, "Order Date", "OrderDate")

    required = {
        "Sales": col_sales, "Profit": col_profit, "Region": col_region,
        "Category": col_category, "Sub-Category": col_subcat, "Customer": col_customer
    }
    missing = [k for k, v in required.items() if v is None]
    if missing:
        st.error(f"Could not find these expected columns in your CSV: {missing}. "
                  f"Actual columns found: {list(df.columns)}")
        st.stop()

    # Standardize names so the rest of the app can use fixed labels
    df = df.rename(columns={
        col_sales: "Sales", col_profit: "Profit", col_region: "Region",
        col_category: "Category", col_subcat: "Sub-Category", col_customer: "Customer Name"
    })
    if col_date:
        df = df.rename(columns={col_date: "Order Date"})
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

    df.dropna(subset=["Sales", "Profit", "Region", "Category", "Sub-Category"], inplace=True)
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
    df.dropna(subset=["Sales", "Profit"], inplace=True)

    return df

df = load_data()

# ---------- Sidebar Filters ----------
st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Region", options=sorted(df["Region"].unique()), default=sorted(df["Region"].unique())
)
categories = st.sidebar.multiselect(
    "Category", options=sorted(df["Category"].unique()), default=sorted(df["Category"].unique())
)
subcategories = st.sidebar.multiselect(
    "Sub-Category",
    options=sorted(df[df["Category"].isin(categories)]["Sub-Category"].unique()),
    default=sorted(df[df["Category"].isin(categories)]["Sub-Category"].unique())
)

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Sub-Category"].isin(subcategories))
]

# ---------- Title ----------
st.title("📊 Global Superstore Business Dashboard")
st.markdown("Analyze sales, profit, and segment-wise performance interactively.")

if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust your selection.")
    st.stop()

# ---------- KPIs ----------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales != 0 else 0
total_orders = filtered_df.shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Profit Margin", f"{profit_margin:.1f}%")
col4.metric("Total Orders", f"{total_orders:,}")

st.markdown("---")

# ---------- Charts Row 1: Sales & Profit by Category ----------
col1, col2 = st.columns(2)

with col1:
    cat_sales = filtered_df.groupby("Category", as_index=False)["Sales"].sum()
    fig1 = px.bar(cat_sales, x="Category", y="Sales", title="Total Sales by Category", color="Category")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    cat_profit = filtered_df.groupby("Category", as_index=False)["Profit"].sum()
    fig2 = px.bar(cat_profit, x="Category", y="Profit", title="Total Profit by Category", color="Category")
    st.plotly_chart(fig2, use_container_width=True)

# ---------- Charts Row 2: Region & Sub-Category ----------
col1, col2 = st.columns(2)

with col1:
    region_sales = filtered_df.groupby("Region", as_index=False)["Sales"].sum()
    fig3 = px.pie(region_sales, names="Region", values="Sales", title="Sales Distribution by Region")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    subcat_profit = filtered_df.groupby("Sub-Category", as_index=False)["Profit"].sum().sort_values("Profit")
    fig4 = px.bar(subcat_profit, x="Profit", y="Sub-Category", orientation="h",
                  title="Profit by Sub-Category", color="Profit", color_continuous_scale="RdYlGn")
    st.plotly_chart(fig4, use_container_width=True)

# ---------- Top 5 Customers ----------
st.markdown("---")
st.subheader("🏆 Top 5 Customers by Sales")

top_customers = (
    filtered_df.groupby("Customer Name", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(5)
)

fig5 = px.bar(top_customers, x="Sales", y="Customer Name", orientation="h",
              title="Top 5 Customers by Sales", color="Sales", color_continuous_scale="Blues")
fig5.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig5, use_container_width=True)

st.dataframe(top_customers, use_container_width=True)

# ---------- Sales Trend Over Time ----------
if "Order Date" in filtered_df.columns:
    st.markdown("---")
    st.subheader("📈 Sales Trend Over Time")

    trend_df = filtered_df.dropna(subset=["Order Date"]).copy()
    trend_df = trend_df.groupby(trend_df["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
    trend_df["Order Date"] = trend_df["Order Date"].dt.to_timestamp()

    fig6 = px.line(trend_df, x="Order Date", y="Sales", title="Monthly Sales Trend")
    st.plotly_chart(fig6, use_container_width=True)

# ---------- Raw Data ----------
with st.expander("View Filtered Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)
