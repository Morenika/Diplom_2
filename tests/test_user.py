import allure
import pytest
import requests


def create_user(base_url, payload):
    return requests.post(f"{base_url}/api/auth/register", json=payload)


@allure.feature("User")
@allure.story("Create user")
class TestCreateUser:

    @allure.title("Создание уникального пользователя — success=True, код 200")
    def test_create_unique_user_success(self, base_url, user_payload):
        response = create_user(base_url, user_payload)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "accessToken" in data
        assert "refreshToken" in data
        assert data["user"]["email"] == user_payload["email"]
        assert data["user"]["name"] == user_payload["name"]

        requests.delete(
            f"{base_url}/api/auth/user",
            headers={"Authorization": data["accessToken"]},
        )

    @allure.title("Создание пользователя, который уже зарегистрирован — код 403 и success=False")
    def test_create_user_that_already_exists(self, base_url, created_user):
        payload = created_user["payload"]

        response = create_user(base_url, payload)

        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False
        assert "message" in data

    @allure.title("Создание пользователя без обязательного поля — код 403 и success=False")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, base_url, user_payload, missing_field):
        payload = user_payload.copy()
        payload.pop(missing_field)

        response = create_user(base_url, payload)

        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False
        assert "message" in data
