import requests
import random
import time

API_URL = "http://127.0.0.1:8001/sensor/add"

sensor_id = 1

while True:
    pressure = random.randint(10, 60)
    flow = random.randint(50, 200)

    data = {
        "sensor_id": sensor_id,
        "pressure": pressure,
        "flow": flow
    }

    try:
        response = requests.post(API_URL, json=data)
        print(response.json())
    except Exception as e:
        print("Error:", e)

    time.sleep(1)