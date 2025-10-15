# Playwright для Python
* Инструкция по использованию фреймворка `Playwright` в `Python` для автоматизации UI тестирования.
---

## Основные особенности
* Playwright - это современный фреймворк для автоматизации браузеров, разработанный Microsoft. Основные особенности:
  * Поддержка Chromium, Firefox и WebKit
  * Кроссплатформенность (Windows, macOS, Linux)
  * Автоматическое ожидание элементов
  * Встроенная поддержка iframe, файловых загрузок, мобильных устройств
  * Возможность эмуляции геолокации, разрешения экрана и других параметров
  * Поддержка параллельного выполнения тестов
  * Встроенный генератор кода (Codegen)
---

## Установка и настройка
* Установка Playwright
```bash
pip install playwright
```
* Существует библиотека прослойка к pytest
* Содержит в себе уже готовый conftest файл, так что его не нужно будет создавать
* Работает не стабильно
```bash
pip install pytest-playwright
```
---
* Установка браузеров (firefox, chromium, webkit)
```bash
playwright install
```
---
* Дополнительные опции установки для установки конкретных браузеров:
```bash
# Основные браузеры
playwright install chromium
playwright install firefox
playwright install webkit
playwright install msedge
# Различные каналы Google Chrome
playwright install chromium --channel=chrome            # Стабильный Chrome
playwright install chromium --channel=chrome-beta       # Бета-версия
playwright install chromium --channel=chrome-dev        # Dev-версия
playwright install chromium --channel=chrome-canary     # Canary-версия (только Windows/macOS)
# Специфичные версии
# Установка конкретной версии (через SHA)
playwright install chromium@<commit-sha>
playwright install firefox@<build-id>
# Использование уже установленных системных браузеров
playwright install chromium --with-deps                 # Установка зависимостей для системного Chromium
```
---
  * Управление браузерами:
```bash
playwright install --list                               # Просмотр установленных версий
playwright install --dry-run                            # Показывает что будет установлено
playwright install --with-deps                          # Устанавливает системные зависимости
playwright install --force                              # Принудительная переустановка
playwright uninstall chromium                           # Удалить браузер
playwright uninstall all                                # Удалить все браузеры
```
---
## Структура и расположение файлов
* Браузеры устанавливаются в:
  * Windows: %USERPROFILE%\AppData\Local\ms-playwright 
  * macOS: ~/Library/Caches/ms-playwright 
  * Linux: ~/.cache/ms-playwright 
* Конфигурационные файлы pytest обычно хранятся в pytest.ini или conftest.py 
* Тесты рекомендуется хранить в директории tests/
* Структура каталогов ресурсов `playwright`:
```commandline
ms-playwright/
  ├── chromium-<version>/       # Папка с браузером chrome
  ├── firefox-<version>/        # Папка с браузером firefox
  ├── webkit-<version>/         # Папка с браузером safari
  ├── ffmpeg/                   # Для работы с видео
  └── cache/                    # Кэш загрузок
```
---

# Фикстуры и начальная настройка
## Базовые фикстуры в `conftest.py`
* Фикстура `playwright`
```python
import pytest
from playwright.sync_api import Playwright, Browser, Page

@pytest.fixture(scope="session")
def playwright() -> Playwright:
    with sync_playwright() as p:
        yield p
```
* Назначение:
  * Инициализация главного объекта Playwright, который управляет всеми браузерами.
* Что делает:
  * Создает экземпляр Playwright через контекстный менеджер sync_playwright()
  * scope="session" означает, что фикстура создается один раз на все время выполнения тестов
  * yield p возвращает объект Playwright для использования в других фикстурах
  * Автоматически закрывает соединение после завершения всех тестов (благодаря with)
---
* Фикстура `browser`
```python
@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Browser:
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()
```
* Назначение:
  * Запуск и управление экземпляром браузера.
* Что делает:
  * Использует объект Playwright из предыдущей фикстуры
  * playwright.chromium.launch() запускает Chromium (можно заменить на firefox или webkit)
  * headless=False - браузер будет видим во время выполнения (для отладки)
  * yield browser возвращает объект Browser для тестов
  * browser.close() гарантирует закрытие браузера после всех тестов
* Важно:
  * scope="session" означает, что все тесты будут использовать один экземпляр браузера (для ускорения). Если нужна изоляция - используйте scope="function".
---
* Фикстура `page`
```python
@pytest.fixture
def page(browser: Browser) -> Page:
    page = browser.new_page()
    yield page
    page.close()
```
* Назначение:
  * Создание новой вкладки (страницы) для каждого теста.
* Что делает:
  * browser.new_page() создает чистую вкладку
  * yield page возвращает объект Page для тестирования
  * page.close() закрывает вкладку после завершения теста
  * По умолчанию scope="function" - новая вкладка для каждого теста
---
* Фикстура `context`
```python
@pytest.fixture
def context(browser: Browser) -> BrowserContext:
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="en-US",
    )
    yield context
    context.close()
```
* Назначение:
  * Создание изолированного контекста браузера с настройками.
* Что делает:
  * browser.new_context() создает новый изолированный контекст (куки, localStorage и др. не пересекаются)
* Параметры:
  * viewport - устанавливает размер окна браузера
  * locale - язык браузера (например, для тестирования локализации)
* Можно добавить другие параметры:
```python
storage_state="auth.json",  # для авторизованных сессий
geolocation={"latitude": 59.93, "longitude": 30.31},
color_scheme="dark",  # темная тема
```
* context.close() очищает все данные контекста после теста
---
* Фикстура `page` с контекстом
```python
@pytest.fixture
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page
    page.close()
```
* Назначение:
  * Создание страницы в подготовленном контексте.
* Что делает:
  * Работает аналогично базовой фикстуре page, но:
  * Использует настроенный контекст вместо дефолтного
  * Все страницы в одном контексте разделяют:
    * Куки
    * Локальное хранилище
    * Настройки viewport/locale
  * Изолированы от страниц в других контекстах
---

* Итоговый пример файла `conftest.py`:
```python
import pytest
from playwright.sync_api import Playwright, Browser, Page, BrowserContext

@pytest.fixture(scope="session")
def playwright() -> Playwright:
    """Главный объект управления Playwright (сессионная фикстура)"""
    with sync_playwright() as playwright_instance:
        yield playwright_instance

@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Browser:
    """Запуск браузера с настройками (сессионная фикстура)"""
    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=500,  # Замедление действий для визуализации
        args=["--start-maximized"]
    )
    yield browser
    browser.close()

@pytest.fixture
def context(browser: Browser) -> BrowserContext:
    """Изолированный контекст браузера с настройками"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="ru-RU",  # Локализация
        timezone_id="Europe/Moscow",  # Часовой пояс
        color_scheme="light",
        permissions=["geolocation"],
        # record_video_dir="videos/"  # Запись видео тестов
    )
    yield context
    context.close()

@pytest.fixture
def page(context: BrowserContext) -> Page:
    """Новая страница в контексте браузера"""
    page = context.new_page()
    yield page
    page.close()
```
---

# Параметризация
* Параметризация браузеров
```python
@pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])
def test_multiple_browsers(browser_name: str, request):
    browser = request.getfixturevalue(browser_name)
    page = browser.new_page()
    # тест
    page.close()
```
---
* Параметризация тестовых данных
```python
@pytest.mark.parametrize("username,password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
])
def test_login(page: Page, username: str, password: str):
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("#login")
```
---

# Основные классы и методы
* Класс Page
```python
# Навигация
page.goto("https://example.com")
page.go_back()
page.go_forward()
page.reload()

# Клики
page.click("button#submit")
page.dblclick("item")
page.hover("menu")

# Ввод текста
page.fill("input#name", "John")
page.type("input#name", "Doe", delay=100)  # с задержкой между символами

# Выбор элементов
page.select_option("select#country", "USA")
page.check("input#agree")
page.uncheck("input#newsletter")

# Ожидания
page.wait_for_selector("div.success")
page.wait_for_url("**/success")
page.wait_for_timeout(1000)  # только в крайних случаях

# Скриншоты
page.screenshot(path="screenshot.png")
page.screenshot(full_page=True)

# Загрузка файлов
with page.expect_file_chooser() as fc:
    page.click("input#upload")
file_chooser = fc.value
file_chooser.set_files("my_file.pdf")
```
---
* Класс ElementHandle
```python
element = page.query_selector("button")
element.click()
element.fill("text")
text = element.text_content()
bounding_box = element.bounding_box()
```
---
* Класс BrowserContext
```python
context = browser.new_context(
    viewport={"width": 1280, "height": 720},
    locale="en-US",
    geolocation={"longitude": 12.492507, "latitude": 41.889938},
    permissions=["geolocation"],
    color_scheme="dark",
)
```
---
* Класс Browser
```python
browser = playwright.chromium.launch(headless=False, slow_mo=50)
browser.close()
```
---
* Асинхронный API
  * Для асинхронного использования импортируйте из playwright.async_api
```python
from playwright.async_api import async_playwright

async def test_example():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        await browser.close()
```
---
* Проверки (Assertions)
```python
from playwright.sync_api import expect

expect(page).to_have_url("https://example.com")
expect(page).to_have_title("Example Domain")
expect(page.locator("h1")).to_have_text("Example Heading")
expect(page.locator("button")).to_be_enabled()
expect(page.locator("div.success")).to_be_visible()
```
---