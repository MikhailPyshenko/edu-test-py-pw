from playwright.sync_api import Page
from config.utils.logger import get_logger


class HelpPage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def get_attribute(self, locator, attr):
        # Получает значение указанного атрибута у элемента
        value = self.page.get_attribute(locator, attr)
        self.logger.info(f"Атрибут '{attr}' элемента {locator}: {value}")
        return value

    def has_class(self, locator, class_name):
        # Проверяет, содержит ли элемент определённый CSS класс
        class_attr = self.page.get_attribute(locator, "class")
        result = class_name in (class_attr or "")
        self.logger.info(f"Элемент {locator} содержит класс '{class_name}': {result}")
        return result

    def get_element_size(self, locator):
        # Получает ширину и высоту элемента
        box = self.page.locator(locator).bounding_box()
        self.logger.info(f"Размер элемента {locator}: {box}")
        return box

    def get_element_position(self, locator):
        # Получает координаты элемента на странице
        box = self.page.locator(locator).bounding_box()
        position = (box["x"], box["y"]) if box else (None, None)
        self.logger.info(f"Координаты элемента {locator}: {position}")
        return position

    def screenshot_element(self, locator, path):
        # Делает скриншот конкретного элемента
        self.logger.info(f"Скриншот элемента {locator} сохраняется в: {path}")
        self.page.locator(locator).screenshot(path=path)

    def wait_until_hidden(self, locator, timeout=5000):
        # Ожидает, пока элемент исчезнет со страницы
        self.logger.info(f"Ожидание, пока элемент {locator} исчезнет (таймаут {timeout} мс)")
        self.page.wait_for_selector(locator, state="hidden", timeout=timeout)
