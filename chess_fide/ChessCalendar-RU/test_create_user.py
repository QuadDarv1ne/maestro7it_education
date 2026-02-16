import requests
import json

# Тест создания пользователя
user_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123",
    "first_name": "Тест",
    "last_name": "Пользователь"
}

response = requests.post(
    "http://localhost:5002/users",
    json=user_data
)

print("Status Code:", response.status_code)
print("Response:", response.json())