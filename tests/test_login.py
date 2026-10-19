
import pytest
from api.login_api import LoginApi
from config.settings import TEST_USERNAME, TEST_PASSWORD
from utils.data_loader import load_json_data
from utils.assertions import assert_api_response

# 创建登录接口对象
login_api = LoginApi()


def test_login_success():
    response = login_api.login(
        username=TEST_USERNAME,
        password=TEST_PASSWORD
    )

    result = assert_api_response(response)

    assert result["data"]["token"] is not None


def test_login_wrong_password():
    response = login_api.login(
        username=TEST_USERNAME,
        password="WrongPassword123"
    )

    result = assert_api_response(
        response,
        expected_code=500
    )

    assert result["message"] == "密码不正确"
    assert result["data"] is None



@pytest.mark.parametrize(
    "case",
    load_json_data("data/login_cases.json"),
    ids=lambda case: case["case_id"]
)
def test_login_invalid_input(case):
    username = (
        TEST_USERNAME
        if case.get("username_source") == "env"
        else case["username"]
    )

    password = (
        TEST_PASSWORD
        if case.get("password_source") == "env"
        else case["password"]
    )

    response = login_api.login(
        username=username,
        password=password
    )

    result = assert_api_response(
        response,
        expected_code=case["expected_code"]
    )

    assert result["message"] in case["expected_messages"]
    assert result["data"] is None
