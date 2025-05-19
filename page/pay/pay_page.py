import allure
from page.base_page import BasePage
from config.actions import ActionPage
from config.asserts import AssertPage
from config.utils.reporter import ReportPage
from page.pay.pay_data import FIRST_NAME, LAST_NAME, ZIP_CODE
from page.pay.pay_locators import (
    FIRST_NAME_INPUT,
    LAST_NAME_INPUT,
    POSTAL_CODE_INPUT,
    CONTINUE_BUTTON,
    FINISH_BUTTON)


class PayPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.actions = ActionPage(page)
        self.asserts = AssertPage(page)
        self.report = ReportPage(page)

    @allure.step(f"Заполнение данных для оплаты")
    def fill_checkout_info(self):
        self.actions.fill(FIRST_NAME_INPUT, FIRST_NAME)
        self.actions.fill(LAST_NAME_INPUT, LAST_NAME)
        self.actions.fill(POSTAL_CODE_INPUT, ZIP_CODE)
        self.actions.click(CONTINUE_BUTTON)

    @allure.step(f"Подтверждение покупки")
    def finish_checkout(self):
        self.actions.click(FINISH_BUTTON)
