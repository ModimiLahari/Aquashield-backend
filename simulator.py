import requests
import time
import random

API_URL = "http://127.0.0.1:8000/sensor/data"

# Use an existing pipe_id from your pipe_network table
PIPE_ID = "550e8400-e29b-41d4-a716-446655440000"

while True:
    payload = {
        "pipe_id": PIPE_ID,
        "flow_rate": round(random.uniform(5, 20), 2),
        "pressure": round(random.uniform(10, 35), 2)
    }

    r = requests.post(API_URL, json=payload)
    print(r.status_code, r.text)

    time.sleep(2)