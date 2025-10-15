import allure
from page.example_base_page import ExampleBasePage
from page.example.example_locators import (
    BUTTON, )
from page.example.example_data import (
    URL,
    TITLE, )


class ExamplePage(ExampleBasePage):
    """Шаблон Page Object"""

    def __init__(self, page):
        super().__init__(page)
        self.base = ExampleBasePage(page)

    @allure.step("Выполнение примера действия")
    def example_scenario(self, INPUT=URL):
        """ Пример теста """
        self.base.logger.info(f"Выполняем пример действия с данными: {URL}")
        # 1. Навигация
        self.base.actions.goto(INPUT)
        # 2. Взаимодействие с элементами
        self.base.actions.wait(100000)
        self.base.actions.click(BUTTON)
        # 3. Проверки
        real_url = self.page.url
        self.base.asserts.url_is(real_url)
        # 4. Отчетность (Скриншот)
        self.base.report.attach_screenshot("Результат выполнения действия")
        # 5. Ожидание (Если нужно)
        self.base.actions.wait(10)
        return self.page


# Пример теста для этого Page Object
def test_example_scenario(page):
    """Пример теста с использованием ExamplePage"""
    example_page = ExamplePage(page)
    # Выполняем действие
    example_page.example_scenario()
    # Дополнительные проверки
    example_page.asserts.title_is(TITLE)
