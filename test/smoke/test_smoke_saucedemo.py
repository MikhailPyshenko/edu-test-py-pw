import pytest
import allure
from page.login.login_page import LoginPage
from page.login.login_data import LOGIN_URL
from page.inventory.inventory_page import InventoryPage
from page.inventory.inventory_data import INVENTORY_URL
from page.cart.cart_page import CartPage
from page.cart.cart_data import *
from page.pay.pay_page import PayPage
from page.pay.pay_data import PAY_URL


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def pay_page(page):
    return PayPage(page)


@pytest.fixture
def login_in_page(login_page):
    login_page.login()
    yield login_page.page
    login_page.logout()


# pytest test/smoke/test_smoke_saucedemo.py::TestSauceDemo --browser=firefox --headless --alluredir=reports/allure-results
@allure.epic("Приложение SauceDemo")
@allure.feature("Дымовые тесты")
class TestSauceDemo:

    # pytest test/smoke/test_smoke_saucedemo.py::TestSauceDemo::test_login_logout --browser=firefox --headless --alluredir=reports/allure-results
    @allure.title("Проверка входа и выхода")
    @allure.description("Проверяет, что пользователь может авторизоваться и выйти из системы")
    @allure.tag("smoke", "auth")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_logout(self, login_page):
        """Проверка входа и выхода"""
        login_page.login()
        with allure.step("Проверяем, что попали на страницу инвентаря"):
            login_page.asserts.url_is(INVENTORY_URL)
        login_page.logout()
        with allure.step("Проверяем, что вернулись на страницу логина"):
            login_page.asserts.url_is(LOGIN_URL)

    # pytest test/smoke/test_smoke_saucedemo.py::TestSauceDemo::test_login_locked --browser=firefox --headless --alluredir=reports/allure-results
    @allure.title("Проверка входа в заблокированного юзера")
    @allure.description("Проверяет, что заблокированный юзер не доступен к логину")
    @allure.tag("smoke", "ban")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_locked(self, login_page):
        """Проверка входа и выхода"""
        login_page.login_locked()
        with allure.step("Проверяем, что остались на странице логина"):
            login_page.asserts.url_is(LOGIN_URL)

    # pytest test/smoke/test_smoke_saucedemo.py::TestSauceDemo::test_product_sorting --browser=firefox --headless
    @allure.title("Проверка сортировки товаров")
    @allure.description("Проверяет сортировку товаров по возрастанию цены")
    @allure.tag("smoke", "inventory")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_product_sorting(self, login_in_page, inventory_page):
        """Проверка сортировки товаров"""
        inventory_page.sort_products_low_to_high()
        # Здесь можно добавить проверку корректности сортировки

    # pytest test/smoke/test_smoke_saucedemo.py::TestSauceDemo::test_add_to_cart --browser=firefox --headless
    @allure.title("Проверка добавления и удаления товаров из корзины")
    @allure.description("Проверяет, что товары добавляются и удаляются из корзины")
    @allure.tag("smoke", "cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_add_to_cart(self, login_in_page, inventory_page):
        """Добавление товаров в корзину"""
        inventory_page.add_products()
        # Проверка увеличения счетчика корзины
        inventory_page.cart_badge_value(2)
        # Удаление продуктов
        inventory_page.remove_products()
        # Проверка отсутствия счетчика корзины
        inventory_page.cart_badge_not_visible()

    # pytest test/smoke/test_smoke_saucedemo.py::TestSauceDemo::test_cart --browser=firefox --headless
    @allure.title("Проверка содержимого и очистки корзины")
    @allure.description("Добавляет товары в корзину, переходит в неё и очищает")
    @allure.tag("smoke", "cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_cart(self, login_in_page, cart_page, inventory_page):
        """Добавление товаров в корзину"""
        inventory_page.add_products()
        inventory_page.go_to_cart()
        # Проверка содержимого корзины
        cart_page.products_in_cart(2)
        # Очистка корзины
        cart_page.remove_products_from_cart()
        # Проверка пустоты в корзине
        cart_page.nothing_in_cart()

    # pytest test/smoke/test_smoke_saucedemo.py::TestSauceDemo::test_checkout_flow --browser=firefox --headless
    @allure.title("Оформление заказа")
    @allure.description("Проходит полный путь оформления заказа с добавлением товара")
    @allure.tag("smoke", "checkout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_checkout_flow(self, login_in_page, inventory_page, cart_page, pay_page):
        """Оформление заказа"""
        # Шаг 1: Добавление товаров
        inventory_page.add_products()
        inventory_page.cart_badge_value(2)
        inventory_page.go_to_cart()
        cart_page.products_in_cart(2)
        # Шаг 2: Оформление
        cart_page.checkout_go_to_pay()
        pay_page.fill_checkout_info()
        pay_page.finish_checkout()
        # Проверка успешного оформления
        with allure.step("Проверка URL успешного завершения покупки"):
            assert "complete" in pay_page.page.url
        # Проверка пустоты в корзине
        cart_page.nothing_in_cart()

    # pytest test/smoke/test_smoke_saucedemo.py::TestSauceDemo::test_full_flow --browser=firefox --headless
    @allure.title("Полный путь пользователя от логина до оформления")
    @allure.description("Smoke: от логина до финального экрана завершения покупки")
    @allure.tag("smokefull", "e2e")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smokefull
    def test_full_flow(self, login_page, inventory_page, cart_page, pay_page):
        """Полный smoke-тест основного потока"""
        # Логин
        login_page.login()
        # Сортировка и добавление товаров
        inventory_page.sort_products_low_to_high()
        inventory_page.add_products()
        inventory_page.cart_badge_value(2)
        inventory_page.go_to_cart()
        cart_page.products_in_cart(2)
        # Оформление заказа
        cart_page.checkout_go_to_pay()
        pay_page.fill_checkout_info()
        pay_page.finish_checkout()
        # Проверки
        login_page.asserts.url_is(PAY_URL)
        # Выход
        login_page.logout()
        login_page.asserts.url_is(LOGIN_URL)
