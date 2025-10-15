import pytest
import allure
from page.demoqa.demoqa_page import DemoqaPage
from page.demoqa.demoqa_data import URL


@pytest.fixture
def demoqa_page(page):
    return DemoqaPage(page)

@pytest.fixture
def demoqa_in_page(demoqa_page):
    demoqa_page.demoqa_scenario()
    yield demoqa_page.page

# pytest test/smoke/test_smoke_demoqa.py::TestDemoqaSmoke --browser=firefox --headless --alluredir=reports/allure-results
class TestDemoqaSmoke:

    # pytest test/smoke/test_smoke_saucedemo.py::TestSauceDemo::test_login_logout --browser=firefox --headless --alluredir=reports/allure-results
    @allure.title("Проверка входа и выхода")
    def test_demoqa_elements(self, demoqa_page):
        """Проверка входа и выхода"""
        demoqa_page.demoqa_scenario()
        demoqa_page.demoqa_text_box()
        demoqa_page.demoqa_check_box()
