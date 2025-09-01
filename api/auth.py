import requests
from config import API_BASE_URL

def login_request(email: str, password: str):
    url = f"{API_BASE_URL}/auth/login"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = f"email={email.lower()}&password={password}"
    response = requests.post(url, headers=headers, data=payload)
    return response
