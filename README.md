# **Шаблон автоматизированного тестирования** 
* Учебный проект (и шаблон) простой автоматизации труда ручного тестирования.
* Основной функционал - UI скрипты на `python` с использованием библиотеки `playwright`.
* В качестве примера автоматизируется проект [saucedemo](https://www.saucedemo.com/v1/)
 
## Подготовка:

<details>
<summary>
==[НАЖМИ]== Ссылки на скачивание и инструкции по настройке среды разработки
</summary><p>

* [Скачать `Python` версии 13+](https://www.python.org/downloads/)
  * [Инструкция установки `Python` глава 2.1, эксплуатация глава 3](https://disk.yandex.ru/edit/d/ziggIjO2lsG0H2023WbIniPegnqahzm72s0qoIz-cKg6UlFmWEZta1prdw)
* [Скачать `git` версии 2.49+](https://git-scm.com/downloads)
  * [Инструкция установки и эксплуатации `git` глава 4.5](https://disk.yandex.ru/i/p6A-v9AiGy5qxA)
* IDE:
  * `OpenIDE` - Российский IDE
    * [Скачать версии 243+](https://openide.ru/download/)
  * `PyCharm` - Рекомендуемый способ взаимодействия с `python`
    * [Скачать версии Community Edition 2024+](https://www.jetbrains.com/ru-ru/pycharm/download/other.html)
    * [Установка глава 2.2 | Эксплуатация глава 4](https://disk.yandex.ru/edit/d/ziggIjO2lsG0H2023WbIniPegnqahzm72s0qoIz-cKg6UlFmWEZta1prdw)
  * `VSCode` - Популярный IDE
    * [Скачать версии 1.99+](https://code.visualstudio.com/docs/?dv=win64user)
</p></details>

* Подробнее в файлах `IDE.md` и `GIT.md`, в папке `docs`, в корневой директории проекта

## **Требования к запуску**
* Описаны в файле `requirements.txt`
* Установка требований из этого файла:
```shell
pip install -r requirements.txt
```
* Альтернативная установка требований:
```shell
pip install playwright pytest pytest-playwright pytest-html allure-pytest requests locust faker
```
* После установки пакетов, установите браузера `playwright`, этой командой установятся 3 (firefox, chromium, webkit) браузера:
  * Подробнее в [docs \ `PW.md`](https://github.com/MikhailPyshenko/edu-test-py-pw/blob/main/docs/PW.md)
```shell
playwright install
```
* Можно указать конкретный браузер (ещё есть msedge, разные версии и прочее) и другие команды:
```shell
playwright install firefox                              # Установить конкретный браузер последней версии
playwright install chromium --channel=chrome-beta       # Установить определенную версию
playwright install --dry-run                            # Показать список установленных браузеров
playwright install --with-deps                          # Установить браузеры для CI (надо sudo)
playwright uninstall chromium                           # Удалить браузер
```

## **Запуск авто-тестов**
* Запуск тестов через `pytest`:
  * Подробнее в [docs \ `PYTEST.md`](https://github.com/MikhailPyshenko/edu-test-py-pw/blob/main/docs/PYTEST.md)
```shell
# Запуск скриптов:
pytest                                              # запустит все фикстуры @pytest в проекте\директории
pytest ПУТЬ/К                                       # запустит все фикстуры @pytest в указанной папке
pytest ПУТЬ/К/ФАЙЛА.py                              # запуск файла с тестами
pytest ПУТЬ/К/ФАЙЛА.py::КЛАСС                       # запуск класса в файле с тестами
pytest ПУТЬ/К/ФАЙЛА.py::КЛАСС::МЕТОД                # запуск метода класса в файле с тестами
# Параметры запуска:
pytest -m smoke # Запуск всех тестов с маркой, т.е. тесты помеченные фикстурой `@pytest.mark.smoke` + регистрация в `pytest.ini` в `markers =`
pytest -m "smoke and regression"                    # Запуск тестов с двумя марками
pytest -m "smoke or regression"                     # Логическое "или"
pytest -m "not slow"                                # Запуск тестов без метки slow
pytest --browser=firefox                            # выбор браузера (chromium, webkit) (если описаны в pytest.ini)
pytest --headless                                   # скрыть браузер (если описаны в pytest.ini)
pytest -k "name"                                    # пуск тестов содержащие в имени введённый текст
pytest -n 4                                         # пуск тестов параллельно (потоки процессора)
pytest --alluredir=reports/allure-results           # пуск тестов с формированием отчета allure (без генерации)
# Прочие параметры запуска:
pytest -v                                           # Подробный вывод (verbose)
pytest -s                                           # Отключить перехват вывода stdout/stderr, полезно для print()
pytest --tb=short                                   # Короткий трейсбек при падении теста
pytest --maxfail=2                                  # Остановиться после 2 падений
pytest --capture=tee-sys                            # Показывать вывод print() и сохранять его
pytest --disable-warnings                           # Отключить предупреждения
pytest --lf                                         # Запустить только упавшие в прошлый раз
pytest --ff                                         # Сначала упавшие, потом остальные
pytest --durations=2                                # Показать (в конце лога итогов прогона) 2 самых медленных теста
# Пример полной команды:
pytest test/smoke/test_smoke_saucedemo.py::TestSauceDemo::test_login_logout --browser=firefox --headless --alluredir=reports/allure-results --durations=2 -v
```

* Просмотр отчёта [`allure`](https://github.com/allure-framework/allure2/releases):
  * Подробнее в [docs \ `ALLURE.md`](https://github.com/MikhailPyshenko/edu-test-py-pw/blob/main/docs/ALLURE.md)
```shell
# Убедитесь в нахождении или перейдите командой CD в главную директорию проекта
# Запустите генерацию отчётов из сырых данных в allure-results, в готовые в allure-report
allure generate reports/allure-results -o reports/allure-report --clean
# Запустите локально хост отчёта
allure open reports/allure-report
# ИЛИ Команда генерации + запуск + удаление
allure serve reports/allure-results
```

## **Покрытые авто-тестами модули**
* **Авторизация** - `page/login/login_page.py`
* **Товары** - `page/inventory/inventory_page.py`
* **Корзина** - `page/cart/cart_page.py`
* **Покупка** - `page/pay/pay_page.py`

## **Архитектура проекта**
* Описание структуры проекта, иерархии файлов и директорий, и их назначение и цель
  * Подробнее в [docs \ `ARCH.md`](https://github.com/MikhailPyshenko/edu-test-py-pw/blob/main/docs/ARCH.md)
<details>
<summary>
==[НАЖМИ]== Структура директорий
</summary><p>

```
/test-projectname/                  # корневой каталог (репозиторий) проекта авто-тестов
├── /page/                          # page object модели
│   ├── /module_page/               # папка с page object моделью и данными модуля
│   │   ├── module_page.py          # page object класс модуля
│   │   ├── module_locators.py      # селекторы элементов модулей
│   │   ├── module_data.py          # тестовые данные модуля
│   │   └── __init__.py
│   ├── example_page.py             # пример построения page object класса
│   ├── base_page.py                # базовый page object класс (основные методы работы со страницей)
│   └── __init__.py
├── /test/                          # тестовые сценарии с группировкой по видам
│   ├── /smoke/                     # дымы (фронт)
│   │   └── test_module.py
│   ├── /accept/                    # приемка (фронт)
│   │   └── test_module.py
│   ├── /api/                       # апи (бэк)
│   │   └── test_module_api.py
│   ├── /load/                      # нагрузочное (locust)
│   │   ├── locust_smoke.py
│   │   └── __init__.py 
│   └── example_test.py             # пример построения тестов
├── /config/                        
│   ├── /utils/                     
│   │   ├── actions.py              # действия
│   │   ├── asserts.py              # проверки
│   │   ├── helpers.py              # вспомогательные методы
│   │   ├── reporter.py             # утилита для отчётов allure
│   │   ├── mock_generator.py       # генерация тестовых данных
│   │   └── __init__.py
│   ├── logger.py                   # конфигурация логирования
│   └── __init__.py
├── /report/                        # отчеты и артефакты (хранятся локально, должно быть подключено хранение в jenkins)
│   ├── /allure-results/            # allure отчеты
│   ├── /pytest-html/               # pytest отчеты (для прикладывания в задачи)
│   ├── /locust/                    # locust отчеты нагрузочного
│   └── /logs/                      # логи выполнения тестов (pytest cli)
├── /docs/                          # документация
│   ├── PLAN.md                     # документация проекта, план автоматизации, тест-кейсы и история изменений
│   ├── CODE.md                     # описание стиля кода в проекте
│   ├── ARCH.md                     # описание вариантов архитектур проекта
│   ├── MD.md                       # описание markdown разметки
│   ├── IDE.md                      # описание работы в различных IDE и их настройки
│   ├── TERMINAL.md                 # описание работы в различных терминалах (cmd\unix\bash)
│   └── GIT.md                      # описание работы с git и bitbucket
├── conftest.py                     # фикстуры pytest для конфигурации тестов и отчетности allure
├── pytest.ini                      # настройки pytest
├── runner.py                       # запускатор для тестовых прогонов
├── requirements.txt                # зависимости
├── README.md                       # описание проекта
└── .gitignore                      # игнор лист git
```
</p></details>

* Отчеты и артефакты папки `report` только для локального хранения, в эксплуатации подразумевается хранение артефактов в `jenkins`.
* Подробнее описано в файле `ARCH.md` в папке `docs` в корневой директории проекта

## **Работа в репозитории**
* **Пример безопасного workflow в `git`**
```shell
# Перед началом работы
git pull origin main

# После нужных изменений и ревью сформируйте инlекс
git add .

# Проверить, что нет лишних файлов
git status

# Создание коммита
git commit -m "Комментарий"

# Отправка изменений на сервер (-u чтобы запомнил ветки, потом можно просто git push)
git push -u origin main
```
* **Подключение к репозиторию через `git`** описано в [docs \ `GIT.md`](https://github.com/MikhailPyshenko/edu-test-py-pw/blob/main/docs/GIT.md)