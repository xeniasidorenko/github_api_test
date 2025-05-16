import os
import requests
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")
API_URL = "https://api.github.com"
print("TOKEN:", TOKEN)

# Заголовки для аутентификации
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def create_repo():
    url = f"{API_URL}/user/repos"
    payload = {
        "name": REPO_NAME,
        "private": False
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"Репозиторий '{REPO_NAME}' успешно создан.")
    elif response.status_code == 422:
        print(f"Репозиторий '{REPO_NAME}' уже существует.")
    else:
        print("[Ошибка при создании репозитория:", response.text)

def check_repo_exists():
    url = f"{API_URL}/users/{USERNAME}/repos"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos = [repo["name"] for repo in response.json()]
        if REPO_NAME in repos:
            print(f"Репозиторий '{REPO_NAME}' найден в списке.")
        else:
            print(f"Репозиторий '{REPO_NAME}' не найден.")
    else:
        print("Ошибка при получении списка репозиториев:", response.text)

def delete_repo():
    url = f"{API_URL}/repos/{USERNAME}/{REPO_NAME}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Репозиторий '{REPO_NAME}' успешно удалён.")
    else:
        print("Ошибка при удалении репозитория:", response.text)

if __name__ == "__main__":
    create_repo()
    check_repo_exists()
    delete_repo()

