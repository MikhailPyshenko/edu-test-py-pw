from playwright.sync_api import Page
from config.utils.logger import get_logger
import allure


class ReportPage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def attach_screenshot(self, name: str = "Screenshot"):
        """Прикрепляет скриншот к отчету Allure."""
        screenshot: bytes = self.page.screenshot()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        self.logger.info(f"Сделали скриншот {name}")
