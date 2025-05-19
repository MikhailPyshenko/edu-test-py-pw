from playwright.sync_api import Page
from config.utils.logger import get_logger


class AssertPage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def url_is(self, expected_url: str):
        # Проверяет, что текущий URL страницы точно совпадает с ожидаемым
        actual_url = self.page.url
        assert actual_url == expected_url, f"Ожидали URL: {expected_url}, получили: {actual_url}"
        self.logger.info(f"URL соответствует ожидаемому: {expected_url}")

    def title_is(self, expected_title: str):
        # Проверяет, что заголовок (title) страницы соответствует ожидаемому
        actual_title = self.page.title()
        assert actual_title == expected_title, f"Ожидали title: {expected_title}, получили: {actual_title}"
        self.logger.info(f"Заголовок страницы соответствует: {expected_title}")

    def element_is_visible(self, locator: str):
        # Проверяет, что элемент отображается (не скрыт) на странице
        assert self.page.is_visible(locator), f"Элемент {locator} должен быть видим"
        self.logger.info(f"Элемент {locator} видим на странице")

    def element_is_hidden(self, locator: str):
        # Проверяет, что элемент скрыт (display: none или не существует в DOM)
        assert self.page.is_hidden(locator), f"Элемент {locator} должен быть скрыт"
        self.logger.info(f"Элемент {locator} скрыт на странице")

    def element_contains_text(self, locator: str, expected_text: str):
        # Проверяет, что элемент содержит указанный текст (частично)
        actual_text = self.page.text_content(locator)
        assert expected_text in (actual_text or ""), f"Элемент {locator} не содержит текст: {expected_text}"
        self.logger.info(f"Элемент {locator} содержит текст: {expected_text}")

    def element_text_is(self, locator: str, expected_text: str):
        # Проверяет, что текст элемента полностью соответствует ожидаемому
        actual_text = self.page.text_content(locator)
        assert actual_text == expected_text, f"Ожидали текст '{expected_text}', получили: '{actual_text}'"
        self.logger.info(f"Текст элемента {locator} точно соответствует: {expected_text}")

    def element_has_attribute(self, locator: str, attr: str, expected_value: str):
        # Проверяет, что значение указанного атрибута элемента соответствует ожидаемому
        actual_value = self.page.get_attribute(locator, attr)
        assert actual_value == expected_value, f"Атрибут '{attr}' должен быть '{expected_value}', получено: '{actual_value}'"
        self.logger.info(f"Атрибут '{attr}' элемента {locator} равен: {expected_value}")

    def element_has_class(self, locator: str, class_name: str):
        # Проверяет, что элемент содержит указанный CSS класс
        classes = self.page.get_attribute(locator, "class") or ""
        assert class_name in classes.split(), f"Элемент {locator} не содержит класс: {class_name}"
        self.logger.info(f"Элемент {locator} содержит класс: {class_name}")

    def element_is_enabled(self, locator: str):
        # Проверяет, что элемент активен (не отключен)
        assert self.page.is_enabled(locator), f"Элемент {locator} должен быть активен"
        self.logger.info(f"Элемент {locator} активен (не disabled)")

    def element_is_disabled(self, locator: str):
        # Проверяет, что элемент отключён (disabled)
        assert not self.page.is_enabled(locator), f"Элемент {locator} должен быть отключён"
        self.logger.info(f"Элемент {locator} отключён (disabled)")

    def element_count_is(self, locator: str, expected_count: int):
        # Проверяет, что количество найденных элементов по локатору совпадает с ожидаемым
        count = self.page.locator(locator).count()
        assert count == expected_count, f"Ожидали {expected_count} элементов {locator}, получили: {count}"
        self.logger.info(f"Найдено {count} элементов {locator} (ожидалось: {expected_count})")

    def element_position_in_list_has_text(
            self,
            list_selector: str,
            position: int,
            expected_text: str,
            item_selector: str = "> div.inventory_item"):
        name_locator = f"{list_selector} {item_selector}:nth-child({position}) .inventory_item_name"
        self.element_text_is(name_locator, expected_text)
