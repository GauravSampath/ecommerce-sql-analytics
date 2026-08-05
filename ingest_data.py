import pandas as pd
import sqlite3
import os

excel_path = "Online Retail.xlsx"
if not os.path.exists(excel_path):
    print(f"Error: Missing dependency '{excel_path}' in runtime execution folder.")
    exit()

print("-> Loading transaction dataset from disk...")
df = pd.read_excel(excel_path)

print("-> Preprocessing columns and transforming targets...")
df = df.dropna(subset=['CustomerID', 'Description'])
df['CustomerID'] = df['CustomerID'].astype(float).astype(int).astype(str)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

# Remove baseline invoice anomalies (returns, negative units)
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

print("-> Initializing relational ingestion sequence (SQLite)...")
conn = sqlite3.connect("ecommerce.db")
df.to_sql("sales", conn, if_exists="replace", index=False)
conn.close()

print("Database pipeline completed. 'ecommerce.db' populated successfully.")
