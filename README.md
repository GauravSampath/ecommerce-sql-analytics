# 📊 Real-Time Event-Driven E-Commerce Analytics Platform

A production-grade, event-driven data streaming pipeline and analytics dashboard built using a microservices architecture. The platform simulates high-velocity storefront transactions, caches concurrent traffic bursts in an in-memory data store to achieve sub-millisecond ingestion latency, and pushes structured data down to disk storage for historical machine learning forecasting.

## 🏗️ System Architecture

1. **The Live Data Stream (`producer.py`):** An event generator simulating erratic storefront checkouts, packaging client transactions into JSON payloads at high frequency.
2. **The High-Speed Cache (`Redis`):** Handles rapid data ingestion as an in-memory message buffer, decoupling incoming website traffic from physical database write limits.
3. **The Live Dashboard UI (`app.py`):** A Streamlit application utilizing isolated visual Fragments to dynamically query the live Redis cache and update charts every second without page lag.
4. **The Storage Syncer (`db_worker.py`):** An independent background process that reads memory snapshots from Redis and safely transfers historical records into a persistent SQLite engine.

## 🛠️ Infrastructure Tech Stack

- **Languages & Frameworks:** Python, Streamlit, SQL
- **Core Caching Engine:** Redis (Key-Value In-Memory Store)
- **Data Engineering:** Pandas, SQLite3
- **Containerization & DevOps:** Docker, Docker Compose

## 📦 How to Launch the Cluster

Ensure Docker Desktop is active on your machine, then open your project root directory and spin up all four interconnected services simultaneously using Docker Compose:

```bash
docker compose up --build
```

Once compilation finishes, open your browser and navigate to:
👉 http://localhost:8585
