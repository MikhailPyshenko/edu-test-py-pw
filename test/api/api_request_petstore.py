import pytest
import requests
import logging
from allure import step, title, feature, story

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://petstore.swagger.io/v2"
HEADERS = {"Content-Type": "application/json"}

PET_ID = 12345
USER_ID = 54321
TEST_USERNAME = "testuser"
UPDATED_USERNAME = "testuser_updated"


@pytest.fixture
def cleanup_pet():
    yield
    response = requests.delete(f"{BASE_URL}/pet/{PET_ID}", headers=HEADERS)
    logger.info(f"Cleanup pet response: {response.status_code}")
    assert response.status_code in [200, 404]


@pytest.fixture
def cleanup_user():
    yield
    for username in [TEST_USERNAME, UPDATED_USERNAME]:
        response = requests.delete(f"{BASE_URL}/user/{username}", headers=HEADERS)
        logger.info(f"Cleanup user {username} response: {response.status_code}")
        assert response.status_code in [200, 404]


@feature("Petstore API Tests")
class TestPetStoreAPI:

    # --- Общие методы ---

    def add_pet(self):
        pet_data = {
            "id": PET_ID,
            "category": {"id": 1, "name": "dogs"},
            "name": "Rex",
            "photoUrls": ["https://example.com/rex.jpg"],
            "tags": [{"id": 1, "name": "friendly"}],
            "status": "available"
        }
        response = requests.post(f"{BASE_URL}/pet", json=pet_data, headers=HEADERS)
        logger.info(f"Add Pet Response: {response.status_code}, {response.text}")
        assert response.status_code == 200
        return response

    def get_pet(self, pet_id=PET_ID):
        response = requests.get(f"{BASE_URL}/pet/{pet_id}", headers=HEADERS)
        logger.info(f"Get Pet Response: {response.status_code}, {response.text}")
        return response

    def delete_pet(self, pet_id=PET_ID):
        response = requests.delete(f"{BASE_URL}/pet/{pet_id}", headers=HEADERS)
        logger.info(f"Delete Pet Response: {response.status_code}, {response.text}")
        return response

    def create_user(self, username=TEST_USERNAME):
        user_data = {
            "id": USER_ID,
            "username": username,
            "firstName": "Test",
            "lastName": "User",
            "email": f"{username}@example.com",
            "password": "password123",
            "phone": "1234567890",
            "userStatus": 0
        }
        response = requests.post(f"{BASE_URL}/user", json=user_data, headers=HEADERS)
        logger.info(f"Create User Response: {response.status_code}, {response.text}")
        assert response.status_code == 200
        return response

    def update_user(self, username=TEST_USERNAME):
        updated_data = {
            "id": USER_ID,
            "username": username,  # username не меняется!
            "firstName": "Updated",
            "lastName": "User",
            "email": "updated@example.com",
            "password": "updated123",
            "phone": "9999999999",
            "userStatus": 2
        }
        response = requests.put(f"{BASE_URL}/user/{username}", json=updated_data, headers=HEADERS)
        logger.info(f"Update User Response: {response.status_code}, {response.text}")
        return response

    def get_user(self, username=TEST_USERNAME):
        response = requests.get(f"{BASE_URL}/user/{username}", headers=HEADERS)
        logger.info(f"Get User Response: {response.status_code}, {response.text}")
        return response

    def delete_user(self, username=TEST_USERNAME):
        response = requests.delete(f"{BASE_URL}/user/{username}", headers=HEADERS)
        logger.info(f"Delete User Response: {response.status_code}, {response.text}")
        return response


    # --- Тесты ---

    @title("Добавление нового питомца")
    @story("Питомцы")
    def test_add_new_pet(self, cleanup_pet):
        with step("Добавляем питомца"):
            response = self.add_pet()
            assert response.json().get("id") == PET_ID

    @title("Получение питомца по ID")
    @story("Питомцы")
    def test_get_pet_by_id(self, cleanup_pet):
        with step("Подготовка - добавляем питомца"):
            self.add_pet()

        with step("Получаем питомца по ID"):
            response = self.get_pet()
            assert response.status_code == 200
            assert response.json().get("id") == PET_ID

    @title("Удаление питомца")
    @story("Питомцы")
    def test_delete_pet(self, cleanup_pet):
        with step("Подготовка - добавляем питомца"):
            self.add_pet()

        with step("Удаляем питомца"):
            response = self.delete_pet()
            assert response.status_code in [200, 404]

    @title("Создание пользователя")
    @story("Пользователи")
    def test_create_user(self, cleanup_user):
        with step("Создаем пользователя"):
            response = self.create_user()
            assert "message" in response.json()

    @title("Получение пользователя по username")
    @story("Пользователи")
    def test_get_user_by_username(self, cleanup_user):
        with step("Подготовка - создаем пользователя"):
            self.create_user()

        with step("Получаем пользователя по username"):
            response = self.get_user()
            assert response.status_code == 200

    @title("Обновление данных пользователя")
    @story("Пользователи")
    def test_update_user(self, cleanup_user):
        # Создаём пользователя
        create_response = self.create_user()
        assert create_response.status_code == 200
        # Проверяем изначальные данные
        get_resp = self.get_user(TEST_USERNAME)
        assert get_resp.status_code == 200
        print("Before update:", get_resp.json())
        # Обновляем пользователя
        update_resp = self.update_user(TEST_USERNAME)
        assert update_resp.status_code == 200
        # Немного подождать (если нужно)
        import time
        time.sleep(1)
        # Получаем данные после обновления
        get_updated_resp = self.get_user(TEST_USERNAME)
        assert get_updated_resp.status_code == 200
        print("After update:", get_updated_resp.json())
        data = get_updated_resp.json()
        assert data["firstName"] == "Updated"

    @title("Аутентификация пользователя")
    @story("Пользователи")
    def test_user_login(self, cleanup_user):
        with step("Подготовка - создаем и обновляем пользователя"):
            self.create_user()
            self.update_user()

        with step("Логинимся под обновленным пользователем"):
            params = {"username": UPDATED_USERNAME, "password": "updated123"}
            response = requests.get(f"{BASE_URL}/user/login", params=params, headers=HEADERS)
            logger.info(f"Login Response: {response.status_code}, {response.text}")
            assert response.status_code == 200
            assert "X-Rate-Limit" in response.headers
            assert "X-Expires-After" in response.headers

    @title("Удаление пользователя")
    @story("Пользователи")
    def test_delete_user(self, cleanup_user):
        username = "temp_user"
        with step("Создаем временного пользователя"):
            user_data = {
                "id": 99999,
                "username": username,
                "firstName": "Temp",
                "lastName": "User",
                "email": "temp@example.com",
                "password": "temp123",
                "phone": "1111111111",
                "userStatus": 1
            }
            response = requests.post(f"{BASE_URL}/user", json=user_data, headers=HEADERS)
            assert response.status_code == 200

        with step("Удаляем временного пользователя"):
            response = requests.delete(f"{BASE_URL}/user/{username}", headers=HEADERS)
            assert response.status_code in [200, 404]
