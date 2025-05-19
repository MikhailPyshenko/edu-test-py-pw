import allure
from page.base_page import BasePage
from config.actions import ActionPage
from config.asserts import AssertPage
from config.utils.reporter import ReportPage
from page.login.login_locators import (
    USERNAME_INPUT,
    PASSWORD_INPUT,
    LOGIN_BUTTON,
    ERROR_MESSAGE_BUTTON,
    MENU_BUTTON,
    LOGOUT_BUTTON)
from page.login.login_data import (
    STANDARD_USER,
    PASSWORD,
    LOGIN_URL,
    LOCKED_USER,
    ERROR_MESSAGE)


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.actions = ActionPage(page)
        self.asserts = AssertPage(page)
        self.report = ReportPage(page)

    @allure.step(f"Логинимся под пользователем: {STANDARD_USER}")
    def login(self, username=STANDARD_USER, password=PASSWORD):
        self.actions.logger.info(f"Логинимся учёткой: {username}")
        self.actions.navigate(LOGIN_URL)
        # Проверяем, что форма логина видима
        self.asserts.element_is_visible(USERNAME_INPUT)
        self.asserts.element_is_visible(PASSWORD_INPUT)
        self.asserts.element_is_visible(LOGIN_BUTTON)
        # Заполняем поля и логинимся
        self.actions.fill(USERNAME_INPUT, username)
        self.actions.fill(PASSWORD_INPUT, password)
        self.actions.click(LOGIN_BUTTON)
        # Проверяем, что авторизация удалась
        self.actions.wait_for_url(f"{LOGIN_URL}inventory.html")
        self.report.attach_screenshot("Итоги логина")
        self.asserts.url_is(f"{LOGIN_URL}inventory.html")

    @allure.step(f"Логинимся под пользователем: {LOCKED_USER}")
    def login_locked(self, username=LOCKED_USER, password=PASSWORD):
        self.actions.logger.info(f"Логинимся ошибочной учёткой: {username}")
        self.actions.navigate(LOGIN_URL)
        # Проверяем, что форма логина видима
        self.asserts.element_is_visible(USERNAME_INPUT)
        self.asserts.element_is_visible(PASSWORD_INPUT)
        self.asserts.element_is_visible(LOGIN_BUTTON)
        # Заполняем поля и логинимся
        self.actions.fill(USERNAME_INPUT, username)
        self.actions.fill(PASSWORD_INPUT, password)
        self.actions.click(LOGIN_BUTTON)
        # Проверяем, что остались на странице логина (т.е. появилась ошибка)
        self.report.attach_screenshot("Итоги логина")
        self.asserts.url_is(LOGIN_URL)
        # Проверяем наличие сообщения об ошибке
        self.asserts.element_is_visible(ERROR_MESSAGE_BUTTON)
        self.asserts.element_contains_text(ERROR_MESSAGE_BUTTON, ERROR_MESSAGE)

    @allure.step("Выход из системы")
    def logout(self):
        self.actions.logger.info("Выход из системы")
        self.actions.click(MENU_BUTTON)
        self.asserts.element_is_visible(LOGOUT_BUTTON)
        self.actions.click(LOGOUT_BUTTON)
        # Проверяем
        self.report.attach_screenshot("Итоги разлогина")
        self.actions.wait_for_url(LOGIN_URL)
        self.asserts.url_is(LOGIN_URL)
