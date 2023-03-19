import streamlit as st
import pandas as pd
import plotly.express as px
from typing import List


page_config = st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

hide_menu_style = "<style> footer {visibility: hidden;} </style>"
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Read the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('input/sales_data_sample.csv', encoding='latin1')
    data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'])
    return data

data = load_data()

# Set the title and sidebar
st.title("Sales Dashboard")
st.sidebar.header("Filters")

# Date range filter

start_date = pd.Timestamp(st.sidebar.date_input("Start date", data['ORDERDATE'].min().date()))
end_date = pd.Timestamp(st.sidebar.date_input("End date", data['ORDERDATE'].max().date()))
filtered_data = data[(data['ORDERDATE'] >= start_date) & (data['ORDERDATE'] <= end_date)]

# Product line filter
product_lines = st.sidebar.multiselect("Product lines", sorted(data['PRODUCTLINE'].unique()), sorted(data['PRODUCTLINE'].unique()))
if product_lines:
    filtered_data = filtered_data[filtered_data['PRODUCTLINE'].isin(product_lines)]

# Country filter
selected_countries = st.sidebar.multiselect("Select Countries", data['COUNTRY'].unique())
if selected_countries:
    filtered_data = filtered_data[filtered_data['COUNTRY'].isin(selected_countries)]


# Order status filter
selected_statuses = st.sidebar.multiselect("Select Order Statuses", data['STATUS'].unique())
if selected_statuses:
    filtered_data = filtered_data[filtered_data['STATUS'].isin(selected_statuses)]


# Calculate KPIs
@st.cache_resource
def calculate_kpis(data: pd.DataFrame) -> List[float]:
    total_sales = data['SALES'].sum()
    total_orders = data['ORDERNUMBER'].nunique()
    average_sales_per_order = total_sales / total_orders
    unique_customers = data['CUSTOMERNAME'].nunique()
    return [total_sales, total_orders, average_sales_per_order, unique_customers]


# Display KPI
def display_kpi(kpi_name: str, kpi_value: float, index: int):
    with st.container():
        st.markdown(f"**{kpi_name}**")
        st.markdown(f"<h1 style='text-align: center; color: {'#f63366' if index % 2 == 0 else '#008080'};'>{kpi_value:,.2f}</h1>", unsafe_allow_html=True)


# Display KPI Metrics
st.header("KPI Metrics")
kpis = calculate_kpis(filtered_data)
kpi_names = ["Total Sales", "Total Orders", "Average Sales per Order", "Unique Customers"]

col1, col2, col3, col4 = st.columns(4)
for i, (kpi_name, kpi_value) in enumerate(zip(kpi_names, kpis)):
    col = col1 if i % 4 == 0 else col2 if i % 4 == 1 else col3 if i % 4 == 2 else col4
    delta = round((kpi_value - kpis[i-1])/kpis[i-1]*100, 2) if i > 0 else 0
    col.metric(label=kpi_name, value=round(kpi_value, 2))



# Sales by product line over time
st.header("Sales by Product Line Over Time")
sales_by_product_line_over_time = filtered_data.groupby(['ORDERDATE', 'PRODUCTLINE'])['SALES'].sum().reset_index()
fig = px.area(sales_by_product_line_over_time, x='ORDERDATE', y='SALES', color='PRODUCTLINE', 
              title="Sales by Product Line over Time", width=900, height=500)
st.plotly_chart(fig)


col1, col2, col3 = st.columns(3)

# Top 10 customers
with col1:
    st.subheader("Top 10 Customers")
    top_customers = filtered_data.groupby('CUSTOMERNAME')['SALES'].sum().reset_index().sort_values('SALES', ascending=False).head(10)
    st.write(top_customers)

# Top 10 products by sales
with col2:
    st.subheader("Top 10 Products by Sales")
    top_products = filtered_data.groupby(['PRODUCTCODE', 'PRODUCTLINE'])['SALES'].sum().reset_index().sort_values('SALES', ascending=False).head(10)
    st.write(top_products)

# Total sales by product line
with col3:
    st.subheader("Total Sales by Product Line")
    total_sales_by_product_line = filtered_data.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
    st.write(total_sales_by_product_line)
