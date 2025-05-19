import allure
import pytest
from page.example.example_page import ExamplePage, TITLE

@pytest.fixture
def example_page(page):
    """Фикстура инициализации страницы"""
    return ExamplePage(page)

@allure.epic("Пример тестового набора")
class TestExampleFlow:

    @allure.title("Пример проверки сценария")
    # @pytest.mark.smoke
    def test_example_page(self, example_page):
        """Пример теста с использованием Page Object"""
        example_page.example_scenario()
        # Дополнительные проверки
        example_page.asserts.title_is(TITLE)
