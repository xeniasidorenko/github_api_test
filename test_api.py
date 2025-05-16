import os
import time
import requests
import pytest
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")
API_URL = "https://api.github.com"

# Заголовки для GitHub API
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Фикстура с данными для всех тестов
@pytest.fixture(scope="module")
def setup_github():
    return {
        "username": USERNAME,
        "token": TOKEN,
        "repo": REPO_NAME,
        "headers": headers,
        "api": API_URL
    }

# Тест создания репозитория
def test_create_repo(setup_github):
    print("\n[ТЕСТ 1] Создание репозитория...")
    time.sleep(10)
    url = f"{setup_github['api']}/user/repos"
    payload = {"name": setup_github["repo"], "private": False}
    response = requests.post(url, headers=setup_github["headers"], json=payload)
    assert response.status_code in [201, 422], f"Ошибка создания: {response.text}"
    if response.status_code == 201:
        print(f"Репозиторий '{setup_github['repo']}' создан.")
    elif response.status_code == 422:
        print(f"Репозиторий '{setup_github['repo']}' уже существует.")

# Тест проверки наличия репозитория
def test_check_repo_exists(setup_github):
    print("\n[ТЕСТ 2] Проверка существования репозитория...")
    time.sleep(10)
    url = f"{setup_github['api']}/users/{setup_github['username']}/repos"
    response = requests.get(url, headers=setup_github["headers"])
    assert response.status_code == 200, f"Ошибка получения списка: {response.text}"
    repo_names = [repo["name"] for repo in response.json()]
    assert setup_github["repo"] in repo_names, f"Репозиторий '{setup_github['repo']}' не найден"
    print(f"Репозиторий '{setup_github['repo']}' найден.")

# Тест удаления репозитория
def test_delete_repo(setup_github):
    print("\n[ТЕСТ 3] Удаление репозитория...")
    time.sleep(10)
    url = f"{setup_github['api']}/repos/{setup_github['username']}/{setup_github['repo']}"
    response = requests.delete(url, headers=setup_github["headers"])
    assert response.status_code == 204, f"Ошибка удаления: {response.text}"
    print(f"Репозиторий '{setup_github['repo']}' удалён.")
