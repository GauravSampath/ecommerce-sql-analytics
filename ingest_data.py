import pandas as pd
import sqlite3
import os

print("⏳ Loading real dataset from Excel (this may take a minute, it is 500k+ rows)...")

# 1. Read the real Excel file
excel_path = "Online Retail.xlsx"
if not os.path.exists(excel_path):
    print(f"❌ Error: Could not find '{excel_path}' in this folder!")
    exit()

df = pd.read_excel(excel_path)

print("🧹 Cleaning data and setting up schema...")

# 2. Basic Cleaning
df = df.dropna(subset=['CustomerID', 'Description']) # Remove empty customers/descriptions
df['CustomerID'] = df['CustomerID'].astype(float).astype(int).astype(str) # Format customer IDs nicely
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']) # Ensure dates are correct

# Calculate total transaction values
df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

# Remove negative values (returns/canceled orders) for clean baseline metrics
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] > 0]

print("🗄️ Ingesting rows into local SQLite database...")

# 3. Connect to SQLite (it creates a file called ecommerce.db automatically)
conn = sqlite3.connect("ecommerce.db")

# 4. Push data into a SQL table named 'sales'
df.to_sql("sales", conn, if_exists="replace", index=False)

# Close connection
conn.close()

print("✅ Success! Created 'ecommerce.db' with real transactions.")
