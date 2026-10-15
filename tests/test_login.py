
import pytest
from api.login_api import LoginApi
from config.settings import TEST_USERNAME, TEST_PASSWORD

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
    "username, password, expected_code, expected_message",
    [
        (
            "not_exist_test_999",
            TEST_PASSWORD,
            404,
            "用户名或密码错误"
        ),
        (
            TEST_USERNAME,
            "",
            404,
            "password不能为空"
        ),
        (
            "",
            TEST_PASSWORD,
            404,
            "username不能为空"
        ),
        (
            "",
            "",
            404,
            ("username不能为空", "password不能为空")
        ),
    ],
    ids=[
        "username_not_exist",
        "password_empty",
        "username_empty",
        "both_empty",
    ]
)
def test_login_invalid_input(
    username,
    password,
    expected_code,
    expected_message
):
    # 使用异常账号或密码进行登录测试
    response = login_api.login(
        username=username,
        password=password
    )

    result = response.json()

    assert response.status_code == 200
    assert result["code"] == expected_code

    if isinstance(expected_message, tuple):
        assert result["message"] in expected_message
    else:
        assert result["message"] == expected_message

    assert result["data"] is None
