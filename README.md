[![Open in Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white)](https://cameronjoejones-streamlit-sales-dashboard-app-3pmk71.streamlit.app/)

# Sales Dashboard

This is a Sales Dashboard built using Streamlit, a popular Python library for building interactive web applications. The dashboard allows you to filter and explore a sales dataset, and visualize key performance metrics, sales by product line over time, and top 10 customers, products, and total sales by product line.

## Prerequisites

To run this dashboard, you need to have Python 3.6 or later installed on your computer, as well as the following libraries:

- Streamlit
- Pandas
- Plotly Express



## How to use

1. Download the `sales_data_sample.csv` file and put it in the `input` folder.
2. Run the script in your terminal or command prompt: `streamlit run app.py`
3. The dashboard will open in your web browser. You can use the filters on the sidebar to explore the dataset and visualize the metrics and charts.

## Features

### Filters

The sidebar of the dashboard includes four filters that allow you to filter the dataset:

- Date range filter: choose a start and end date to filter by the order date.
- Product line filter: select one or more product lines to filter by.
- Country filter: select one or more countries to filter by.
- Order status filter: select one or more order statuses to filter by.

### KPI Metrics

The dashboard displays four key performance indicators (KPIs) for the filtered dataset:

- Total sales
- Total orders
- Average sales per order
- Unique customers

The KPIs are displayed in a metric format with the current value and percentage change from the previous value.

### Sales by Product Line Over Time

This chart displays the total sales by product line over time. You can hover over the chart to see the details for a specific date and product line.

### Top 10 Customers, Products, and Total Sales by Product Line

These tables display the top 10 customers, products, and total sales by product line for the filtered dataset.


3. The dashboard will open in your web browser. You can use the filters on the sidebar to explore the dataset and visualize the metrics and charts.

## Features

### Filters

The sidebar of the dashboard includes four filters that allow you to filter the dataset:

- Date range filter: choose a start and end date to filter by the order date.
- Product line filter: select one or more product lines to filter by.
- Country filter: select one or more countries to filter by.
- Order status filter: select one or more order statuses to filter by.

### KPI Metrics

The dashboard displays four key performance indicators (KPIs) for the filtered dataset:

- Total sales
- Total orders
- Average sales per order
- Unique customers

The KPIs are displayed in a metric format with the current value and percentage change from the previous value.

### Sales by Product Line Over Time

This chart displays the total sales by product line over time. You can hover over the chart to see the details for a specific date and product line.

### Top 10 Customers, Products, and Total Sales by Product Line

These tables display the top 10 customers, products, and total sales by product line for the filtered dataset.
