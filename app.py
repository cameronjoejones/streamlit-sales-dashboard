import streamlit as st
import pandas as pd
import plotly.express as px
from typing import List

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)


@st.cache_data
def load_data():
    data = pd.read_csv('input/sales_data_sample.csv', encoding='latin1')
    data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'])
    return data


data = load_data()

st.title("📊 Sales Dashboard")
st.sidebar.header("Filters")

start_date = pd.Timestamp(st.sidebar.date_input("Start date", data['ORDERDATE'].min().date()))
end_date = pd.Timestamp(st.sidebar.date_input("End date", data['ORDERDATE'].max().date()))

filtered_data = data[(data['ORDERDATE'] >= start_date) & (data['ORDERDATE'] <= end_date)]


def filter_data(data, column, values):
    return data[data[column].isin(values)] if values else data


product_lines = sorted(data['PRODUCTLINE'].unique())
selected_product_lines = st.sidebar.multiselect("Product lines", product_lines, product_lines)
filtered_data = filter_data(filtered_data, 'PRODUCTLINE', selected_product_lines)

selected_countries = st.sidebar.multiselect("Select Countries", data['COUNTRY'].unique())
filtered_data = filter_data(filtered_data, 'COUNTRY', selected_countries)

selected_statuses = st.sidebar.multiselect("Select Order Statuses", data['STATUS'].unique())
filtered_data = filter_data(filtered_data, 'STATUS', selected_statuses)

st.sidebar.info('Created by Cameron Jones')

st.sidebar.markdown("""
<div style='display: flex; justify-content: center; align-items: center;'>
  <a href="https://github.com/cameronjoejones/streamlit-sales-dashboard.git" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-181717.svg?style=for-the-badge&logo=GitHub&logoColor=white" alt="GitHub Badge">
  </a>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def calculate_kpis(data: pd.DataFrame) -> List[float]:
    total_sales = data['SALES'].sum()
    sales_in_m = f"{total_sales / 1000000:.2f}M"
    total_orders = data['ORDERNUMBER'].nunique()
    average_sales_per_order = f"{total_sales / total_orders / 1000:.2f}K"
    unique_customers = data['CUSTOMERNAME'].nunique()
    return [sales_in_m, total_orders, average_sales_per_order, unique_customers]


st.header("KPI Metrics")
kpis = calculate_kpis(filtered_data)
kpi_names = ["Total Sales", "Total Orders", "Average Sales per Order", "Unique Customers"]

for i, (col, (kpi_name, kpi_value)) in enumerate(zip(st.columns(4), zip(kpi_names, kpis))):
    col.metric(label=kpi_name, value=kpi_value)

combined_data = filtered_data.groupby(['ORDERDATE', 'PRODUCTLINE'])['SALES'].sum().reset_index()
sales_by_product_line_over_time = filtered_data.groupby(['ORDERDATE', 'PRODUCTLINE'])['SALES'].sum().reset_index()

combine_product_lines = st.checkbox("Combine Product Lines", value=True)

if combine_product_lines == True:
    fig = px.area(combined_data, x='ORDERDATE', y='SALES',
                  title="Sales by Product Line Over Time", width=900, height=500)
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    fig.update_xaxes(rangemode='tozero', showgrid=False)
    fig.update_yaxes(rangemode='tozero', showgrid=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = px.area(sales_by_product_line_over_time, x='ORDERDATE', y='SALES', color='PRODUCTLINE',
                  title="Sales by Product Line Over Time", width=900, height=500)
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    fig.update_xaxes(rangemode='tozero', showgrid=False)
    fig.update_yaxes(rangemode='tozero', showgrid=True)
    st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Top 10 Customers")
    top_customers = filtered_data.groupby('CUSTOMERNAME')['SALES'].sum().reset_index().sort_values('SALES',
                                                                                                   ascending=False).head(
        10)
    st.write(top_customers)

with col2:
    st.subheader("Top 10 Products by Sales")
    top_products = filtered_data.groupby(['PRODUCTCODE', 'PRODUCTLINE'])['SALES'].sum().reset_index().sort_values(
        'SALES', ascending=False).head(10)
    st.write(top_products)

with col3:
    st.subheader("Total Sales by Product Line")
    total_sales_by_product_line = filtered_data.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
    st.write(total_sales_by_product_line)
