from playwright.sync_api import Page
from config.utils.logger import get_logger

HOME_URL = "https://www.saucedemo.com/"
HEADER_TITLE = ".title"
BURGER_MENU = "#react-burger-menu-btn"


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def goto_home(self):
        self.page.goto(HOME_URL)

    def burger_menu(self):
        self.page.click(BURGER_MENU)
