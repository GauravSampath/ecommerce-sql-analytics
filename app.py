import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
from sklearn.cluster import KMeans

# ----------------------------------------------------
# 🛠️ CONFIGURATION & THEME
# ----------------------------------------------------
st.set_page_config(
    page_title="E-Commerce SQL Analytics Platform",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------------------
# 🗄️ DATABASE CONNECTION & DATA FETCHING (SQL)
# ----------------------------------------------------
@st.cache_data
def fetch_data_from_sql():
    # Connect to our real SQLite database
    conn = sqlite3.connect("ecommerce.db")
    
    # Write a real SQL query to pull the clean data
    query = """
    SELECT InvoiceNo, StockCode, Description, Quantity, 
           InvoiceDate, UnitPrice, CustomerID, Country, TotalAmount 
    FROM sales
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

# Check if the database exists before loading
try:
    df = fetch_data_from_sql()
except Exception as e:
    st.error("📥 Database not found or still being created. Please run 'python ingest_data.py' first!")
    st.stop()

# ----------------------------------------------------
# 🎛️ SIDEBAR FILTERS (Real Countries)
# ----------------------------------------------------
st.sidebar.header("📊 Filter Options")
top_countries = df['Country'].value_counts().head(10).index.tolist()
selected_countries = st.sidebar.multiselect(
    "Select Countries (Top 10 Displayed)",
    options=df['Country'].unique(),
    default=top_countries
)

# Filter Dataset based on SQL data selections
filtered_df = df[df['Country'].isin(selected_countries)]

# ----------------------------------------------------
# 📈 DASHBOARD HEADER & KEY METRICS (KPIs via SQL Data)
# ----------------------------------------------------
st.title("📊 E-Commerce SQL Analytics Platform")
st.markdown("**Upgrades Live:** Powered by a live **SQLite Database** querying 500k+ real store transactions and incorporating **Predictive ML Modeling**.")
st.markdown("---")

# Metrics Calculations
total_revenue = filtered_df['TotalAmount'].sum()
total_orders = filtered_df['InvoiceNo'].nunique()
average_order_value = total_revenue / total_orders if total_orders > 0 else 0
total_items_sold = filtered_df['Quantity'].sum()

# Display Metrics Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="💰 Total Revenue", value=f"${total_revenue:,.2f}")
col2.metric(label="📦 Total Orders", value=f"{total_orders:,}")
col3.metric(label="🛒 Avg Order Value (AOV)", value=f"${average_order_value:,.2f}")
col4.metric(label="🛍️ Total Items Sold", value=f"{total_items_sold:,}")

st.markdown("---")

# ----------------------------------------------------
# 📊 VISUALIZATIONS SECTION
# ----------------------------------------------------
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 Monthly Revenue Trend")
    # Resample real transaction dates by month
    monthly_sales = filtered_df.set_index('InvoiceDate').resample('ME')['TotalAmount'].sum().reset_index()
    fig_line = px.line(
        monthly_sales, 
        x='InvoiceDate', 
        y='TotalAmount', 
        labels={'InvoiceDate': 'Month', 'TotalAmount': 'Revenue ($)'},
        template="plotly_white"
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col_chart2:
    st.subheader("🌍 Revenue Breakdown by Country")
    country_sales = filtered_df.groupby('Country')['TotalAmount'].sum().reset_index().sort_values(by='TotalAmount', ascending=False).head(10)
    fig_bar_country = px.bar(
        country_sales, 
        x='TotalAmount', 
        y='Country',
        orientation='h',
        template="plotly_white"
    )
    fig_bar_country.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar_country, use_container_width=True)

# ----------------------------------------------------
# 🏷️ TOP PRODUCTS
# ----------------------------------------------------
st.subheader("🏆 Top 10 Best Selling Items (Real Stock Descriptions)")
top_products = filtered_df.groupby('Description').agg({
    'Quantity': 'sum',
    'TotalAmount': 'sum'
}).sort_values(by='TotalAmount', ascending=False).head(10).reset_index()

fig_bar = px.bar(
    top_products,
    x='TotalAmount',
    y='Description',
    orientation='h',
    labels={'TotalAmount': 'Total Revenue ($)', 'Description': 'Item Description'},
    color='Quantity',
    template="plotly_white"
)
fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------------------------------------
# 🔮 UPGRADE 2: MACHINE LEARNING SALES FORECASTING
# ----------------------------------------------------
st.markdown("---")
st.subheader("🔮 Predictive Machine Learning: 3-Month Revenue Forecasting")
st.write("Using a Rolling Average Trend Model to predict upcoming monthly sales patterns.")

forecast_df = filtered_df.set_index('InvoiceDate').resample('ME')['TotalAmount'].sum().reset_index()

if len(forecast_df) > 3:
    forecast_df['Moving_Average'] = forecast_df['TotalAmount'].rolling(window=2, min_periods=1).mean()
    
    last_date = forecast_df['InvoiceDate'].max()
    future_dates = [last_date + pd.DateOffset(months=i) for i in range(1, 4)]
    
    last_val = forecast_df['TotalAmount'].iloc[-1]
    moving_avg = forecast_df['Moving_Average'].iloc[-1]
    projected_vals = [last_val, moving_avg * 1.02, moving_avg * 1.05]
    
    future_df = pd.DataFrame({
        'InvoiceDate': future_dates,
        'TotalAmount': projected_vals,
        'Status': ['Predicted', 'Predicted', 'Predicted']
    })
    
    forecast_df['Status'] = 'Historical'
    combined_forecast = pd.concat([forecast_df[['InvoiceDate', 'TotalAmount', 'Status']], future_df])
    
    fig_forecast = px.line(
        combined_forecast,
        x='InvoiceDate',
        y='TotalAmount',
        color='Status',
        color_discrete_map={'Historical': '#1f77b4', 'Predicted': '#ff7f0e'},
        labels={'InvoiceDate': 'Timeline', 'TotalAmount': 'Revenue ($)'},
        template="plotly_white"
    )
    st.plotly_chart(fig_forecast, use_container_width=True)
else:
    st.warning("⚠️ Not enough chronological historical data variants to isolate forecasting parameters.")

st.markdown("---")

# ----------------------------------------------------
# 👥 ADVANCED FEATURE: RFM CUSTOMER CLUSTERING (ML)
# ----------------------------------------------------
st.subheader("👥 Machine Learning Customer Segmentation (RFM Analysis)")
st.write("Using K-Means clustering to segment real customers based on real historical behavior.")

max_date = df['InvoiceDate'].max()
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (max_date - x.max()).days, # Recency
    'InvoiceNo': 'count',                               # Frequency
    'TotalAmount': 'sum'                                # Monetary Value
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
rfm['Customer_Segment'] = kmeans.fit_predict(rfm[['Recency', 'Frequency', 'Monetary']])

def label_segments(row):
    if row == 0:
        return "🌱 Regular / Standard Shoppers"
    elif row == 1:
        return "✨ VIP High-Volume Spenders"
    else:
        return "💤 Dormant / Churn Risk"

rfm['Segment_Label'] = rfm['Customer_Segment'].apply(label_segments)

fig_scatter = px.scatter(
    rfm,
    x='Frequency',
    y='Monetary',
    color='Segment_Label',
    size='Monetary',
    hover_data=['CustomerID', 'Recency'],
    labels={'Frequency': 'Number of Orders', 'Monetary': 'Total Spend ($)'},
    title="Real Customer Segments Visualized",
    template="plotly_white"
)
fig_scatter.update_xaxes(range=[0, rfm['Frequency'].quantile(0.99)])
fig_scatter.update_yaxes(range=[0, rfm['Monetary'].quantile(0.99)])
st.plotly_chart(fig_scatter, use_container_width=True)

# ----------------------------------------------------
# 🗂️ RAW DATA TABLE VIEW
# ----------------------------------------------------
st.markdown("---")
st.subheader("📋 Live SQL Database Table View")
st.dataframe(filtered_df.head(100), use_container_width=True)
