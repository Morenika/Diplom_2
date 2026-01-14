import allure
import requests


def update_user(base_url, headers=None, payload=None):
    return requests.patch(f"{base_url}/api/auth/user", headers=headers, json=payload)


@allure.feature("User")
@allure.story("Update user")
class TestUpdateUser:

    @allure.title("Изменение email с авторизацией — success=True, код 200")
    def test_update_email_with_auth_success(self, base_url, auth_headers, created_user):
        new_email = "updated_" + created_user["payload"]["email"]
        payload = {"email": new_email}

        response = update_user(base_url, headers=auth_headers, payload=payload)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["user"]["email"] == new_email

    @allure.title("Изменение имени с авторизацией — success=True, код 200")
    def test_update_name_with_auth_success(self, base_url, auth_headers):
        payload = {"name": "Updated Name"}

        response = update_user(base_url, headers=auth_headers, payload=payload)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["user"]["name"] == "Updated Name"

    @allure.title("Изменение пароля с авторизацией — success=True, код 200")
    def test_update_password_with_auth_success(self, base_url, auth_headers):
        payload = {"password": "new_password_123"}

        response = update_user(base_url, headers=auth_headers, payload=payload)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True

    @allure.title("Изменение email без авторизации — success=False, код 401")
    def test_update_email_without_auth_fail(self, base_url):
        payload = {"email": "noauth@test.ru"}

        response = update_user(base_url, headers=None, payload=payload)

        assert response.status_code == 401
        data = response.json()

        assert data["success"] is False
        assert "message" in data

    @allure.title("Изменение имени без авторизации — success=False, код 401")
    def test_update_name_without_auth_fail(self, base_url):
        payload = {"name": "Hacker"}

        response = update_user(base_url, headers=None, payload=payload)

        assert response.status_code == 401
        data = response.json()

        assert data["success"] is False
        assert "message" in data

    @allure.title("Изменение пароля без авторизации — success=False, код 401")
    def test_update_password_without_auth_fail(self, base_url):
        payload = {"password": "hack_password"}

        response = update_user(base_url, headers=None, payload=payload)

        assert response.status_code == 401
        data = response.json()

        assert data["success"] is False
        assert "message" in data
