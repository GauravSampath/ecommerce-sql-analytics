# 📊 E-Commerce SQL Analytics & Predictive Platform

A production-grade, containerized data analytics dashboard built entirely in Python. The platform ingests real-world transaction logs, stores them in a relational schema, and runs statistical machine learning models to deliver actionable business intelligence.

## 🚀 Core Features
- **Relational SQL Storage:** Migrated architecture from local mockups to a structured SQLite engine querying 500k+ transaction records.
- **Predictive ML Engines:** Integrates Scikit-Learn K-Means clustering for customer segmentation and rolling time-series trend vectors for 3-month sales forecasting.
- **Environment Isolation:** Containerized via Docker to ensure reliable, cross-platform local workspace replication.

## 🛠️ Tech Stack
- **Languages:** Python, SQL
- **Libraries:** Pandas, NumPy, Scikit-Learn, Plotly, Streamlit
- **DevOps/Databases:** Docker, SQLite3

## 📦 How to Run Locally

### 1. Ingest and Process Data
Run the ETL script to parse, clean, and populate the local relational database:
```bash
python ingest_data.py
```

### 2. Launch the Analytics App
Start the background engine and access the interface on your network port:
```bash
python -m streamlit run app.py --server.port 8585
```
Open your browser and navigate to `http://localhost:8585`.
