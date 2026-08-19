import streamlit as st
import redis
import json
import pandas as pd

st.set_page_config(page_title="Real-Time E-Commerce Engine", layout="wide")
st.title("📊 Real-Time Storefront Analytics Dashboard")
st.markdown("---")

r = redis.Redis(host='redis', port=6379, db=0)



# Fragment wrapper ensures smooth UI updates every 1 second
@st.fragment(run_every=1.0)
def render_live_metrics():
    raw_data = r.lrange("ecommerce_stream", 0, -1)
    
    if not raw_data:
        st.info("⌛ Awaiting transaction stream feeds from Redis...")
        return

    transactions = [json.loads(item.decode('utf-8')) for item in raw_data]
    df = pd.DataFrame(transactions)
    df['Time'] = pd.to_datetime(df['timestamp'], unit='s')

    total_sales = len(df)
    total_revenue = df["amount"].sum()

    col1, col2 = st.columns(2)
    col1.metric(label="📈 Live Stream Sales Volume", value=f"{total_sales} orders")
    col2.metric(label="💰 Cached Revenue Velocity", value=f"${total_revenue:,.2f}")

    st.markdown("### 📉 Rolling Transactions Timeline")
    # Streamlit updated chart property config to fix warnings
    timeline_df = df.set_index('Time').resample('5s')['amount'].sum().fillna(0)

    st.line_chart(timeline_df, use_container_width=True)



render_live_metrics()

