import redis
import sqlite3
import json
import time

# Connect to the internal Redis container network address
r = redis.Redis(host='redis', port=6379, db=0)

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS live_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL,
    product TEXT,
    amount REAL,
    user_id INTEGER
)
""")
conn.commit()

print("💾 SQL Storage Archiver is syncing records from Redis...")

# Keep track of the last processed index to prevent duplicate entries
last_processed_idx = 0

while True:
    # Read the full sliding window queue from Redis memory safely
    raw_logs = r.lrange("ecommerce_stream", last_processed_idx, -1)
    
    if raw_logs:
        for raw_log in raw_logs:
            data = json.loads(raw_log.decode('utf-8'))
            
            cursor.execute("""
            INSERT INTO live_logs (timestamp, product, amount, user_id)
            VALUES (?, ?, ?, ?)
            """, (data['timestamp'], data['product'], data['amount'], data['user_id']))
            
            conn.commit()
            print(f"📦 Archived data row: {data['product']} - ${data['amount']}")
            last_processed_idx += 1
    
    # If the queue was trimmed by the producer, reset our tracking index pointer
    current_queue_len = r.llen("ecommerce_stream")
    if current_queue_len < last_processed_idx:
        last_processed_idx = max(0, current_queue_len - 10)
        
    time.sleep(1) # Sleep briefly to protect host CPU cycles
