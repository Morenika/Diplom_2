import allure

from api.auth_api import login_user
from constants import LOGIN_ERROR_MESSAGE


@allure.feature("Auth")
@allure.story("Login user")
class TestLoginUser:

    @allure.title("Логин существующего пользователя — success=True, код 200")
    def test_login_user_success(self, created_user):
        payload = {
            "email": created_user["payload"]["email"],
            "password": created_user["payload"]["password"],
        }

        response = login_user(payload)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "accessToken" in data
        assert "refreshToken" in data
        assert data["user"]["email"] == payload["email"]

    @allure.title("Логин с неверным паролем — success=False, код 401")
    def test_login_user_with_wrong_password(self, created_user):
        payload = {
            "email": created_user["payload"]["email"],
            "password": "wrong_password",
        }

        response = login_user(payload)

        assert response.status_code == 401
        data = response.json()

        assert data["success"] is False
        assert data["message"] == LOGIN_ERROR_MESSAGE
