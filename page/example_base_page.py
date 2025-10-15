# Импорты:
from playwright.sync_api import Page  # Базовый класс Page из Playwright
from config.utils.logger import get_logger  # Логгер для записи событий
from config.actions import ActionPage  # Класс с методами действий (клики, ввод текста и т.д.)
from config.asserts import AssertPage  # Класс с проверками (assertions)
from config.utils.reporter import ReportPage  # Инструменты для отчетности (скриншоты, видео и т.д.)
from config.utils.helpers import HelpPage  # Вспомогательные инструменты

# Константы страницы:
PAGE_URL = "https://www.example.com/"  # Уникальный URL страницы (если есть)


class ExampleBasePage:
    """ ШАБЛОН класса Page Object Model. Содержит: Локаторы. URL страницы. Инициализацию зависимостей (logger, actions, asserts, reporter) """

    def __init__(self, page: Page):
        """Инициализация страницы браузера и зависимости."""
        self.page = page  # Основной объект Playwright
        self.logger = get_logger(self.__class__.__name__)  # Логгер с именем класса
        self.actions = ActionPage(page)  # Методы действий (клик, ввод текста и т.д.)
        self.asserts = AssertPage(page)  # Методы проверок
        self.report = ReportPage(page)  # Инструменты для отчетов (allure, скриншоты)
        self.help = HelpPage(page)  # Вспомогательные инструменты

    def goto(self):
        """Переход на страницу по URL. Записывает событие в лог."""
        self.actions.goto(PAGE_URL)  # переход на страницу
        self.logger.info(f"Открыта страница: {PAGE_URL}")  # пример добавления логирования в метод
