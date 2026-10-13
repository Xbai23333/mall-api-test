
import requests
import pytest
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("MALL_BASE_URL")
TEST_USERNAME = os.getenv("MALL_TEST_USERNAME")
TEST_PASSWORD = os.getenv("MALL_TEST_PASSWORD")

def test_login_success():
    url = f"{BASE_URL}/admin/login"

    data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }

    response = requests.post(url, json=data)

    result = response.json()

    assert response.status_code == 200
    assert result["code"] == 200
    assert result["data"]["token"] is not None



def test_login_wrong_password():
    url = f"{BASE_URL}/admin/login"

    data = {
        "username": TEST_USERNAME,
        "password": "WrongPassword123"
    }

    response = requests.post(url, json=data)
    result = response.json()

    assert response.status_code == 200
    assert result["code"] == 500
    assert result["message"] == "密码不正确"
    assert result["data"] is None



@pytest.mark.parametrize(
    "username, password, expected_code, expected_message",
    [
        ("not_exist_test_999", TEST_PASSWORD, 404, "用户名或密码错误"),
        (TEST_USERNAME, "", 404, "password不能为空"),
        ("", TEST_PASSWORD, 404, "username不能为空"),
        ("", "", 404, ("username不能为空", "password不能为空")),
    ],
    ids=[
        "username_not_exist",
        "password_empty",
        "username_empty",
        "both_empty",
    ]
)


def test_login_invalid_input(username, password, expected_code, expected_message):
    url = f"{BASE_URL}/admin/login"

    data = {
        "username": username,
        "password": password
    }

    response = requests.post(url, json=data)
    result = response.json()


    assert response.status_code == 200
    assert result["code"] == expected_code

    if isinstance(expected_message, tuple):
        assert result["message"] in expected_message
    else:
        assert result["message"] == expected_message

    assert result["data"] is None