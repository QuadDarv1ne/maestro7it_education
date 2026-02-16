import requests
import json

# Тест парсинга CFR
parse_data = {
    "year": 2026
}

response = requests.post(
    "http://localhost:5003/parse/cfr",
    json=parse_data
)

print("Status Code:", response.status_code)
print("Response:", response.json())