import requests
import json

# Тест аутентификации
auth_data = {
    "username": "testuser",
    "password": "testpassword123"
}

response = requests.post(
    "http://localhost:5002/auth/login",
    json=auth_data
)

print("Status Code:", response.status_code)
print("Response:", response.json())