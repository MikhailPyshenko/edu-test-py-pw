from playwright.sync_api import Page
from config.utils.logger import get_logger


class ActionPage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def goto(self, url):
        # Переходит на указанный URL
        self.logger.info(f"Переход по URL: {url}")
        self.page.goto(url)

    def click(self, locator):
        # Кликает по элементу с заданным локатором
        self.logger.info(f"Клик по элементу: {locator}")
        self.page.click(locator)

    def fill(self, locator, text):
        # Заполняет поле с заданным локатором текстом
        self.logger.info(f"Заполнение поля {locator} текстом: {text}")
        self.page.fill(locator, text)

    def select_option(self, locator, value):
        # Выбирает значение из селектора с выпадающим списком
        self.logger.info(f"Выбор значения '{value}' в селекторе {locator}")
        self.page.select_option(locator, value=value)

    def wait_for_url(self, url):
        # Ждёт появления заданного URL
        self.logger.info(f"Ожидание загрузки URL: {url}")
        self.page.wait_for_url(url)

    def hover(self, locator):
        # Наводит курсор мыши на элемент
        self.logger.info(f"Наведение на элемент: {locator}")
        self.page.hover(locator)

    def get_text(self, locator):
        # Получает текстовое содержимое элемента
        text = self.page.text_content(locator)
        self.logger.info(f"Получен текст из {locator}: {text}")
        return text

    def is_visible(self, locator):
        # Проверяет, виден ли элемент на странице
        visible = self.page.is_visible(locator)
        self.logger.info(f"Элемент {locator} видим: {visible}")
        return visible

    def is_enabled(self, locator):
        # Проверяет, активен ли элемент (не disabled)
        enabled = self.page.is_enabled(locator)
        self.logger.info(f"Элемент {locator} активен: {enabled}")
        return enabled

    def wait_for_selector(self, locator, timeout=5000):
        # Ждёт появления элемента с заданным локатором (5000 тикетов = 5 секунд)
        self.logger.info(f"Ожидание селектора {locator} в течение {timeout} мс")
        self.page.wait_for_selector(locator, timeout=timeout)

    def wait(self, timeout_seconds):
        """Ждёт указанное количество секунд"""
        self.logger.info(f"Ожидание {timeout_seconds} секунд")
        self.page.wait_for_timeout(timeout_seconds * 1000)  # конвертируем секунды в миллисекунды

    def wait_load_all(self, load_opt):
        # Ждёт загрузки, варианты: Только DOM без ресов "domcontentloaded", полная загрузка всего "load", отсутствие сетевых запросов дольше 500 мс "networkidle"
        # Словарь для понятного описания вариантов загрузки
        load_descriptions = {
            "domcontentloaded": "DOM (без ресурсов)",
            "load": "полной загрузки всего контента",
            "networkidle": "отсутствия сетевых запросов",
        }
        description = load_descriptions.get(load_opt, f"неизвестного типа: {load_opt}")
        self.logger.info(f"Ожидание загрузки страницы: {description}")
        self.page.wait_for_load_state(load_opt)

    def wait_load_all_js(self):
        self.logger.info(f"JavaScript-способ ожидания загрузки: ждем, пока DOM полностью загрузится")
        self.page.wait_for_function("document.readyState === 'complete'")
