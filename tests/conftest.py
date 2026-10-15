
import pytest
from api.login_api import LoginApi
from config.settings import TEST_USERNAME, TEST_PASSWORD


@pytest.fixture(scope="module")
def auth_headers():
    # 创建登录接口对象
    login_api = LoginApi()

    # 登录管理员账号，获取Token
    response = login_api.login(
        username=TEST_USERNAME,
        password=TEST_PASSWORD
    )

    # 验证登录请求成功
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    token = result["data"]["token"]
    token_head = result["data"]["tokenHead"]

    # 返回带有Token的请求头
    return {
        "Authorization": token_head + token
    }
