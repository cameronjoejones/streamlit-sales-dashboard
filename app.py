from typing import List, Tuple

import pandas as pd
import plotly.express as px
import streamlit as st


def set_page_config():
    st.set_page_config(
        page_title="Sales Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)


@st.cache_data
def load_data() -> pd.DataFrame:
    data = pd.read_csv('data/sales_data_sample.csv', encoding='latin1')
    data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'])
    return data


def filter_data(data: pd.DataFrame, column: str, values: List[str]) -> pd.DataFrame:
    return data[data[column].isin(values)] if values else data


@st.cache_data
def calculate_kpis(data: pd.DataFrame) -> List[float]:
    total_sales = data['SALES'].sum()
    sales_in_m = f"{total_sales / 1000000:.2f}M"
    total_orders = data['ORDERNUMBER'].nunique()
    average_sales_per_order = f"{total_sales / total_orders / 1000:.2f}K"
    unique_customers = data['CUSTOMERNAME'].nunique()
    return [sales_in_m, total_orders, average_sales_per_order, unique_customers]


def display_kpi_metrics(kpis: List[float], kpi_names: List[str]):
    st.header("KPI Metrics")
    for i, (col, (kpi_name, kpi_value)) in enumerate(zip(st.columns(4), zip(kpi_names, kpis))):
        col.metric(label=kpi_name, value=kpi_value)


def display_sidebar(data: pd.DataFrame) -> Tuple[List[str], List[str], List[str]]:
    st.sidebar.markdown(
    """
    <a href="https://twitter.com/cameronjoejones" target="_blank" style="text-decoration: none;">
        <div style="display: flex; align-items: center;">
            <img src="https://abs.twimg.com/icons/apple-touch-icon-192x192.png" width="30" height="30">
            <span style="font-size: 16px; margin-left: 5px;">Follow me on Twitter</span>
        </div>
    </a>
    """, unsafe_allow_html=True
    )
    st.sidebar.header("Filters")
    start_date = pd.Timestamp(st.sidebar.date_input("Start date", data['ORDERDATE'].min().date()))
    end_date = pd.Timestamp(st.sidebar.date_input("End date", data['ORDERDATE'].max().date()))

    product_lines = sorted(data['PRODUCTLINE'].unique())
    selected_product_lines = st.sidebar.multiselect("Product lines", product_lines, product_lines)

    selected_countries = st.sidebar.multiselect("Select Countries", data['COUNTRY'].unique())

    selected_statuses = st.sidebar.multiselect("Select Order Statuses", data['STATUS'].unique())

    st.sidebar.info('Created by Cameron Jones')



    return selected_product_lines, selected_countries, selected_statuses


def display_charts(data: pd.DataFrame):
    combine_product_lines = st.checkbox("Combine Product Lines", value=True)

    if combine_product_lines:
        fig = px.area(data, x='ORDERDATE', y='SALES',
                      title="Sales by Product Line Over Time", width=900, height=500)
    else:
        fig = px.area(data, x='ORDERDATE', y='SALES', color='PRODUCTLINE',
                      title="Sales by Product Line Over Time", width=900, height=500)

    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    fig.update_xaxes(rangemode='tozero', showgrid=False)
    fig.update_yaxes(rangemode='tozero', showgrid=True)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Top 10 Customers")
        top_customers = data.groupby('CUSTOMERNAME')['SALES'].sum().reset_index().sort_values('SALES',
                                                                                              ascending=False).head(10)
        st.write(top_customers)

    with col2:
        st.subheader("Top 10 Products by Sales")
        top_products = data.groupby(['PRODUCTCODE', 'PRODUCTLINE'])['SALES'].sum().reset_index().sort_values('SALES',
                                                                                                             ascending=False).head(
            10)
        st.write(top_products)

    with col3:
        st.subheader("Total Sales by Product Line")
        total_sales_by_product_line = data.groupby('PRODUCTLINE')['SALES'].sum().reset_index()
        st.write(total_sales_by_product_line)


def main():
    set_page_config()

    data = load_data()

    st.title("📊 Sales Dashboard")

    selected_product_lines, selected_countries, selected_statuses = display_sidebar(data)

    filtered_data = data.copy()
    filtered_data = filter_data(filtered_data, 'PRODUCTLINE', selected_product_lines)
    filtered_data = filter_data(filtered_data, 'COUNTRY', selected_countries)
    filtered_data = filter_data(filtered_data, 'STATUS', selected_statuses)

    kpis = calculate_kpis(filtered_data)
    kpi_names = ["Total Sales", "Total Orders", "Average Sales per Order", "Unique Customers"]
    display_kpi_metrics(kpis, kpi_names)

    display_charts(filtered_data)


if __name__ == '__main__':
    main()
