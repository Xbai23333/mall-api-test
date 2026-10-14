
import os

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("MALL_BASE_URL", "http://localhost:8080")


@pytest.fixture(scope="module")
def auth_headers():
    # 登录管理员账号，获取 Token
    response = requests.post(
        f"{BASE_URL}/admin/login",
        json={
            "username": os.getenv("MALL_TEST_USERNAME"),
            "password": os.getenv("MALL_TEST_PASSWORD")
        },
        timeout=10
    )

    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    token = result["data"]["token"]
    token_head = result["data"]["tokenHead"]

    # 返回带有 Token 的请求头
    return {
        "Authorization": token_head + token
    }
