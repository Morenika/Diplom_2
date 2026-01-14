import uuid

import pytest
import requests

from constants import BASE_URL

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture
def browser(request):
    return request.config.getoption("--browser")

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser name: chrome or firefox",
    )


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser name: chrome or firefox"
    )

@pytest.fixture
def user_payload():
    unique = uuid.uuid4().hex[:8]
    return {
        "email": f"user_{unique}@test.ru",
        "password": "password123",
        "name": f"User_{unique}",
    }


@pytest.fixture()
def created_user(user_payload):
    # create
    r = requests.post(f"{BASE_URL}/api/auth/register", json=user_payload)
    assert r.status_code == 200, f"Can't create user: {r.status_code} {r.text}"
    data = r.json()
    assert data.get("success") is True

    access_token = data.get("accessToken")
    assert access_token, f"No accessToken in response: {data}"

    yield {"payload": user_payload, "access_token": access_token}

    # cleanup
    requests.delete(
        f"{BASE_URL}/api/auth/user",
        headers={"Authorization": access_token},
    )


@pytest.fixture
def auth_headers(created_user):
    token = created_user["access_token"]
    return {"Authorization": token}


@pytest.fixture
def ingredients():
    return requests.get(f"{BASE_URL}/api/ingredients")


@pytest.fixture
def ingredient_ids(ingredients):
    data = ingredients.json()
    return [item["_id"] for item in data["data"]]
