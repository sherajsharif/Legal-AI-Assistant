import requests
response = requests.post(
    "http://127.0.0.1:8000/chat",
    json={"prompt": "Free legal aid kaise milegi?"}
)
print(response.json())