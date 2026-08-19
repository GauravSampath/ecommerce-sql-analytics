import redis
import json
import time
import random

# Connect to the local Redis container cache
r = redis.Redis(host='redis', port=6379, db=0)




products = ["Laptop", "Smartphone", "Headphones", "Smartwatch", "Keyboard"]

print("⚡ Streaming live transactions to Redis...")
while True:
    transaction = {
        "timestamp": time.time(),
        "product": random.choice(products),
        "amount": round(random.uniform(15.0, 1500.0), 2),
        "user_id": random.randint(10000, 99999)
    }
    
    # Append the live purchase data straight into Redis memory
    r.rpush("ecommerce_stream", json.dumps(transaction))
    r.ltrim("ecommerce_stream", -200, -1) # Keep memory clean
    
    time.sleep(random.uniform(0.1, 0.7))
