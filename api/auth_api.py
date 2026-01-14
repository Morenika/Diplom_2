import requests

from constants import BASE_URL

LOGIN_ENDPOINT = "/api/auth/login"


def login_user(payload):
    return requests.post(
        f"{BASE_URL}{LOGIN_ENDPOINT}",
        json=payload
    )
