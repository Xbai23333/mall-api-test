
import pytest
from api.login_api import LoginApi
from config.settings import TEST_USERNAME, TEST_PASSWORD
from utils.data_loader import load_json_data

# 创建登录接口对象
login_api = LoginApi()


def test_login_success():
    # 使用正确的管理员账号和密码登录
    response = login_api.login(
        username=TEST_USERNAME,
        password=TEST_PASSWORD
    )

    result = response.json()

    assert response.status_code == 200
    assert result["code"] == 200
    assert result["data"]["token"] is not None


def test_login_wrong_password():
    # 使用错误密码登录
    response = login_api.login(
        username=TEST_USERNAME,
        password="WrongPassword123"
    )

    result = response.json()

    assert response.status_code == 200
    assert result["code"] == 500
    assert result["message"] == "密码不正确"
    assert result["data"] is None



@pytest.mark.parametrize(
    "case",
    load_json_data("data/login_cases.json"),
    ids=lambda case: case["case_id"]
)
def test_login_invalid_input(case):
    # 根据JSON数据准备测试账号
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

    # 发送登录请求
    response = login_api.login(
        username=username,
        password=password
    )

    result = response.json()

    # 验证HTTP状态码
    assert response.status_code == 200

    # 验证业务状态码
    assert result["code"] == case["expected_code"]

    # 验证错误提示
    assert result["message"] in case["expected_messages"]

    # 验证异常登录没有返回用户数据
    assert result["data"] is None
