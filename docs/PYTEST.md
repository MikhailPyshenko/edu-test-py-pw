## 📌 Установка

```bash
pip install pytest
```

---

## 🚀 Запуск тестов

- Все тесты:
  ```bash
  pytest
  ```

- Конкретный файл:
  ```bash
  pytest tests/test_login.py
  ```

- С выводом:
  ```bash
  pytest -v
  ```

- Только помеченные (см. `@pytest.mark.<name>`):
  ```bash
  pytest -m "smoke"
  ```

- С отчетом:
  ```bash
  pytest --html=report.html
  ```

---

## ✅ Структура проекта

```
project/
│
├── tests/
│   ├── test_login.py
│   ├── test_cart.py
│
├── conftest.py       # фикстуры
├── requirements.txt
└── pytest.ini        # конфиг
```

---

## 🔧 Фикстуры

**`conftest.py`:**

```python
import pytest

@pytest.fixture
def sample_user():
    return {"name": "admin", "password": "1234"}
```

**`test_example.py`:**

```python
def test_user_login(sample_user):
    assert sample_user["name"] == "admin"
```

---

## 🧪 Маркировки

```python
import pytest

@pytest.mark.smoke
def test_main_page():
    assert True

@pytest.mark.regression
def test_login():
    assert True
```

**Запуск по метке:**

```bash
pytest -m "smoke"
```

---

## ⚙️ pytest.ini

```ini
[pytest]
markers =
    smoke: основные проверки
    regression: регрессионные тесты
addopts = -v --tb=short
```

---

## 📁 Параметризация

```python
import pytest

@pytest.mark.parametrize("a,b,result", [
    (2, 3, 5),
    (1, 5, 6),
])
def test_add(a, b, result):
    assert a + b == result
```

---

## 📷 Скриншоты, отчеты

- HTML отчет:
  ```bash
  pip install pytest-html
  pytest --html=report.html
  ```

- Allure:
  ```bash
  pip install allure-pytest
  pytest --alluredir=allure-results
  allure serve allure-results
  ```

---

## 🔁 Повтор запуска упавших тестов

```bash
pip install pytest-rerunfailures
pytest --reruns 2
```

---

## 🧹 Часто используемые плагины

```bash
pip install pytest-cov pytest-xdist pytest-rerunfailures pytest-mock
```

---

## 🔄 Параллельный запуск

```bash
pip install pytest-xdist
pytest -n auto
```

---

## ⛔ Skip, xfail

```python
import pytest

@pytest.mark.skip(reason="не актуально")
def test_old():
    ...

@pytest.mark.xfail
def test_bug():
    assert 1 == 2
```

---

## 📚 Примеры команд

```bash
pytest tests/test_login.py::test_valid_login
pytest -v --maxfail=2
pytest --tb=short
pytest --disable-warnings
```

---

## 📎 Полезные ссылки

- Документация: https://docs.pytest.org/en/stable/
- PyPI: https://pypi.org/project/pytest/
- Allure: https://docs.qameta.io/allure/
