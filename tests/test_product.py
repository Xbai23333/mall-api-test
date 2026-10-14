
import os
import pytest

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("MALL_BASE_URL", "http://localhost:8080")

@pytest.fixture
def auth_headers():
    # 登录获取 Token
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




def test_product_list_success(auth_headers):
    # 第一步：查询商品列表
    response = requests.get(
        f"{BASE_URL}/product/list",
        headers=auth_headers,
        params={
            "pageNum": 1,
            "pageSize": 5
        },
        timeout=10
    )

    # 第二步：验证返回结果
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    data = result["data"]

    assert data["pageNum"] == 1
    assert data["pageSize"] == 5
    assert isinstance(data["list"], list)
    assert len(data["list"]) <= 5
    assert data["total"] >= len(data["list"])




def test_product_list_page_two(auth_headers):
    # 查询第二页，每页3条商品
    response = requests.get(
        f"{BASE_URL}/product/list",
        headers=auth_headers,
        params={
            "pageNum": 2,
            "pageSize": 3
        },
        timeout=10
    )

    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    data = result["data"]

    assert data["pageNum"] == 2
    assert data["pageSize"] == 3
    assert isinstance(data["list"], list)
    assert len(data["list"]) <= 3

    if data["total"] >= 6:
        assert len(data["list"]) == 3




def test_product_list_search_keyword(auth_headers):
    # 按关键词查询商品
    response = requests.get(
        f"{BASE_URL}/product/list",
        headers=auth_headers,
        params={
            "keyword": "华为",
            "pageNum": 1,
            "pageSize": 10
        },
        timeout=10
    )

    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    products = result["data"]["list"]

    assert isinstance(products, list)
    assert len(products) > 0

    for product in products:
        assert "华为" in product["name"]




def test_product_list_without_token():
    # 第一步：不携带 Token，直接请求商品列表
    response = requests.get(
        f"{BASE_URL}/product/list",
        params={
            "pageNum": 1,
            "pageSize": 5
        },
        timeout=10
    )

    # 第二步：检查 HTTP 状态码
    assert response.status_code == 200

    # 第三步：检查业务状态码
    result = response.json()
    assert result["code"] == 401

    # 第四步：检查错误提示
    assert "暂未登录" in result["message"]


def test_product_list_page_zero(auth_headers):
    # 边界值测试：页码为0
    response = requests.get(
        f"{BASE_URL}/product/list",
        headers=auth_headers,
        params={
            "pageNum": 0,
            "pageSize": 5
        },
        timeout=10
    )

    # 验证当前接口的实际响应行为
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    data = result["data"]

    assert data["pageNum"] == 0
    assert data["pageSize"] == 5
    assert data["total"] == 20
    assert data["list"] == []


def test_product_list_negative_page(auth_headers):
    # 边界值测试：页码为负数
    response = requests.get(
        f"{BASE_URL}/product/list",
        headers=auth_headers,
        params={
            "pageNum": -1,
            "pageSize": 5
        },
        timeout=10
    )

    # 验证当前接口的实际响应
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    data = result["data"]

    assert data["pageNum"] == -1
    assert data["pageSize"] == 5
    assert isinstance(data["list"], list)
    assert data["list"] == []


def test_product_list_page_size_zero(auth_headers):
    # 边界值测试：每页商品数量为0
    response = requests.get(
        f"{BASE_URL}/product/list",
        headers=auth_headers,
        params={
            "pageNum": 1,
            "pageSize": 0
        },
        timeout=10
    )

    # 验证当前接口的实际响应
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    data = result["data"]

    assert data["pageNum"] == 1
    assert data["pageSize"] == 0
    assert data["totalPage"] == 0
    assert data["list"] == []


def test_product_list_negative_page_size(auth_headers):
    # 边界值测试：每页商品数量为负数
    response = requests.get(
        f"{BASE_URL}/product/list",
        headers=auth_headers,
        params={
            "pageNum": 1,
            "pageSize": -1
        },
        timeout=10
    )

    # 验证当前接口的实际响应
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    data = result["data"]

    assert data["pageNum"] == 1
    assert data["pageSize"] == -1
    assert data["totalPage"] == 0
    assert data["list"] == []