import allure
from page.base_page import BasePage
from config.actions import ActionPage
from config.asserts import AssertPage
from config.utils.reporter import ReportPage
from page.cart.cart_locators import CHECKOUT_BUTTON, CART_LIST, CART_ITEM
from page.inventory.inventory_locators import *


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.actions = ActionPage(page)
        self.asserts = AssertPage(page)
        self.report = ReportPage(page)

    @allure.step(f"Проверяем заполненность корзины")
    def products_in_cart(self, expected_count: int = None):
        self.report.attach_screenshot("Товары в корзине")
        self.asserts.element_is_visible(CART_LIST)
        # Проверка количества товаров
        if expected_count is not None:
            self.asserts.element_count_is(CART_ITEM, expected_count)
        # Проверка наличия товаров
        self.asserts.element_is_visible(f"{CART_ITEM} >> nth=0")

    @allure.step(f"Проверяем пустоту корзины")
    def nothing_in_cart(self):
        self.report.attach_screenshot("Пустота в корзине")
        self.asserts.element_count_is(CART_ITEM, 0)
        self.asserts.element_is_hidden(CART_ITEM)

    @allure.step(f"Удаляем продукт из корзины")
    def remove_products_from_cart(self):
        self.actions.click(REMOVE_FROM_CART_1)
        self.actions.click(REMOVE_FROM_CART_2)

    @allure.step(f"Переход к покупке")
    def checkout_go_to_pay(self):
        self.actions.click(CHECKOUT_BUTTON)
