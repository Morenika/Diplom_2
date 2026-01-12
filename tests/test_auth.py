import allure
import requests


def login_user(base_url, payload):
    return requests.post(f"{base_url}/api/auth/login", json=payload)


@allure.feature("Auth")
@allure.story("Login user")
class TestLoginUser:

    @allure.title("Логин существующего пользователя — success=True, код 200")
    def test_login_user_success(self, base_url, created_user):
        payload = {
            "email": created_user["payload"]["email"],
            "password": created_user["payload"]["password"],
        }

        response = login_user(base_url, payload)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "accessToken" in data
        assert "refreshToken" in data
        assert data["user"]["email"] == payload["email"]

    @allure.title("Логин с неверным паролем — success=False, код 401")
    def test_login_user_with_wrong_password(self, base_url, created_user):
        payload = {
            "email": created_user["payload"]["email"],
            "password": "wrong_password",
        }

        response = login_user(base_url, payload)

        assert response.status_code == 401
        data = response.json()

        assert data["success"] is False
        assert "message" in data
