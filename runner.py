import subprocess
import os

# Путь к директории с результатами Allure
allure_results_dir = "reports/allure-results"

# Команда запуска pytest
command_pytest = [
    "pytest",
    "test/smoke/test_smoke_saucedemo.py",
    "--browser=firefox",
    "--headless",
    "--alluredir=" + allure_results_dir,
]

command_allure = [
    "allure",
    "serve",
    allure_results_dir,
]

# Запуск тестов
result = subprocess.run(command_pytest)
# Сборка отчета
report = subprocess.run(command_allure)

# Код завершения
exit(result.returncode)
