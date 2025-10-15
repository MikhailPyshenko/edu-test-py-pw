import allure
from page.example_base_page import ExampleBasePage
from page.demoqa.demoqa_locators import (
    BUTTON,
    TEXT_BOX,
    SUBMIT, )
from page.demoqa.demoqa_data import URL, URL_ELEM, URL_TEXT_BOX, TITLE


class DemoqaPage(ExampleBasePage):
    """Шаблон Page Object"""

    def __init__(self, page):
        super().__init__(page)
        self.base = ExampleBasePage(page)

    @allure.step("Выполнение примера действия")
    def demoqa_scenario(self, INPUT=URL):
        """ Пример теста """
        self.base.logger.info(f"Выполняем пример действия с данными: {INPUT}")
        # 1. Навигация
        self.base.page.goto(INPUT, wait_until="domcontentloaded")
        # 2. Взаимодействие с элементами
        self.base.actions.click(BUTTON)
        # 3. Проверки
        self.base.asserts.url_is(URL_ELEM)
        # 4. Отчетность (Скриншот)
        self.base.report.attach_screenshot("Результат выполнения действия")
        # 5. Ожидание (Если нужно)
        self.base.actions.wait(4000)
        return self.page

    @allure.step("Выполнение примера действия")
    def demoqa_text_box(self, INPUT=URL_ELEM):
        """ Пример теста """
        self.base.logger.info(f"Выполняем пример действия с данными: {INPUT}")
        # 2. Взаимодействие с элементами
        self.base.actions.click(TEXT_BOX)
        self.base.actions.click(TEXT_BOX)
        self.base.actions.fill("#userName", "Mike")
        self.base.actions.fill("#userEmail", "Mike_ne@mail.ru")
        self.base.actions.fill("#currentAddress", "Mike avenue 123")
        self.base.actions.fill("#permanentAddress", "Mike www.leningrad.ru")
        self.base.actions.click(SUBMIT)
        # 3. Проверки
        self.base.asserts.url_is(URL_TEXT_BOX)
        self.base.asserts.element_contains_text("#name", "Mike")
        # 4. Отчетность (Скриншот)
        self.base.report.attach_screenshot("Результат выполнения действия")
        # 5. Ожидание (Если нужно)
        self.base.actions.wait(4)
        return self.page

    @allure.step("Выполнение примера действия")
    def demoqa_check_box(self, INPUT=URL_ELEM):
        """ Пример теста """
        self.base.logger.info(f"Выполняем пример действия с данными: {INPUT}")
        # 2. Взаимодействие с элементами
        self.base.actions.click("#item-1 > span")
        self.base.actions.click("#tree-node > ol > li > span > button > svg")
        self.base.page.check("#tree-node > ol > li > ol > li:nth-child(2) > span > label > span.rct-checkbox > svg")
        # 3. Проверки
        assert self.base.page.is_checked("#tree-node > ol > li > ol > li:nth-child(2) > span > label > span.rct-checkbox > svg")
        # 4. Отчетность (Скриншот)
        self.base.report.attach_screenshot("Результат выполнения действия")
        # 5. Ожидание (Если нужно)
        self.base.actions.wait(4)
        return self.page

# Пример теста для этого Page Object
def test_demoqa_scenario(page):
    """Пример теста с использованием ExamplePage"""
    demoqa = DemoqaPage(page)
    # Выполняем действие
    demoqa.demoqa_scenario()
    demoqa.demoqa_text_box()
    demoqa.demoqa_check_box()
    # Дополнительные проверки
    demoqa.asserts.title_is(TITLE)
