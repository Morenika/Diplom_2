import os
import uuid
import pytest
import requests

BASE_URL = os.getenv(
    "STELLAR_BURGERS_API_URL",
    "https://stellarburgers.education-services.ru"
)


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def user_payload():
    unique = uuid.uuid4().hex[:8]
    return {
        "email": f"user_{unique}@test.ru",
        "password": "password123",
        "name": f"User_{unique}"
    }
@pytest.fixture()
def created_user(base_url, user_payload):
    # create
    r = requests.post(f"{base_url}/api/auth/register", json=user_payload)
    assert r.status_code == 200, f"Can't create user: {r.status_code} {r.text}"
    data = r.json()
    assert data.get("success") is True

    access_token = data.get("accessToken")
    assert access_token, f"No accessToken in response: {data}"

    yield {"payload": user_payload, "access_token": access_token}

    # cleanup
    requests.delete(
        f"{base_url}/api/auth/user",
        headers={"Authorization": access_token},
    )
@pytest.fixture
def auth_headers(created_user):
    token = created_user["access_token"]
    return {"Authorization": token}

@pytest.fixture
def ingredients(base_url):
    response = requests.get(f"{base_url}/api/ingredients")
    return response

@pytest.fixture
def ingredient_ids(ingredients):
    data = ingredients.json()
    return [item["_id"] for item in data["data"]]

