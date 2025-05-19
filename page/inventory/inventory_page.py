import allure
from playwright.sync_api import expect
from page.base_page import BasePage
from config.actions import ActionPage
from config.asserts import AssertPage
from config.utils.reporter import ReportPage
from page.inventory.inventory_locators import (
    SORT_DROPDOWN,
    INVENTORY_LIST,
    ADD_TO_CART_1,
    ADD_TO_CART_2,
    REMOVE_FROM_CART_1,
    REMOVE_FROM_CART_2,
    SHOPPING_CART_BADGE,
    SHOPPING_CART)
from page.inventory.inventory_data import SORT_OPTION_VALUE, FIRST_ITEM_POST_SORT_LOHI


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.actions = ActionPage(page)
        self.asserts = AssertPage(page)
        self.report = ReportPage(page)

    @allure.step(f"Сортировка по цене от дешевых к дорогим")
    def sort_products_low_to_high(self):
        self.actions.select_option(SORT_DROPDOWN, SORT_OPTION_VALUE)
        self.report.attach_screenshot("Итоги сортировки лохи")
        self.asserts.element_position_in_list_has_text(INVENTORY_LIST, 1, FIRST_ITEM_POST_SORT_LOHI)

    @allure.step(f"Добавление продуктов {ADD_TO_CART_1, ADD_TO_CART_2} в корзину")
    def add_products(self):
        self.actions.click(ADD_TO_CART_1)
        self.actions.click(ADD_TO_CART_2)
        self.report.attach_screenshot("Итоги добавления товаров")

    @allure.step(f"Удаление продуктов {ADD_TO_CART_1, ADD_TO_CART_2} из корзины на странице товаров")
    def remove_products(self):
        self.actions.click(REMOVE_FROM_CART_1)
        self.actions.click(REMOVE_FROM_CART_2)
        self.report.attach_screenshot("Итоги удаления товаров")

    @property
    def cart_badge(self):
        return self.page.locator(SHOPPING_CART_BADGE)

    def cart_badge_value(self, value):
        expect(self.cart_badge).to_have_text(str(value))

    def cart_badge_not_visible(self):
        expect(self.cart_badge).not_to_be_visible()

    @allure.step(f"Переход в корзину")
    def go_to_cart(self):
        self.actions.click(SHOPPING_CART)
