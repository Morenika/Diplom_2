import allure
import requests

from constants import BASE_URL

@allure.feature("Orders")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами — success=True")
    def test_create_order_with_auth_and_ingredients_success(self, base_url, auth_headers, ingredient_ids):
        payload = {"ingredients": ingredient_ids[:2]}
        response = requests.post(f"{BASE_URL}/api/orders", json=payload, headers=auth_headers)

        assert response.status_code == 200
        body = response.json()
        assert body.get("success") is True
        assert "order" in body

    @allure.title("Создание заказа без авторизации, но с ингредиентами — success=True")
    def test_create_order_without_auth_with_ingredients_success(self, base_url, ingredient_ids):
        payload = {"ingredients": ingredient_ids[:2]}
        response = requests.post(f"{BASE_URL}/api/orders", json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body.get("success") is True
        assert "order" in body

    @allure.title("Создание заказа с невалидным хешем ингредиента — 400 и ошибка")
    def test_create_order_with_invalid_ingredient_hash_bad_request(self, base_url):
        payload = {"ingredients": ["invalid_hash"]}
        response = requests.post(f"{BASE_URL}/api/orders", json=payload)

        assert response.status_code == 400
        body = response.json()
        assert body.get("success") is False

@allure.feature("Orders")
class TestGetUserOrders:

    @allure.title("Получение заказов авторизованного пользователя — success=True")
    def test_get_orders_with_auth_success(self, base_url, auth_headers):
        response = requests.get(f"{BASE_URL}/api/orders", headers=auth_headers)

        assert response.status_code == 200
        body = response.json()
        assert body.get("success") is True
        assert "orders" in body

    @allure.title("Получение заказов без авторизации — ошибка")
    def test_get_orders_without_auth_unauthorized(self, base_url):
        response = requests.get(f"{BASE_URL}/api/orders")

        assert response.status_code in (401, 403) 
        body = response.json()
        assert body.get("success") is False
