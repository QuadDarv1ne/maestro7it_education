import requests
import json

# Тест создания турнира
tournament_data = {
    "name": "Чемпионат России 2026",
    "start_date": "2026-03-15",
    "end_date": "2026-03-25",
    "location": "Москва",
    "category": "National Championship",
    "description": "Ежегодный чемпионат России по шахматам"
}

response = requests.post(
    "http://localhost:5001/tournaments",
    json=tournament_data
)

print("Status Code:", response.status_code)
print("Response:", response.json())