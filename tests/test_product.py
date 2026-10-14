
import os
import pytest

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("MALL_BASE_URL", "http://localhost:8080")


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




@pytest.mark.parametrize(
    "page_num, page_size",
    [
        (0, 5),
        (-1, 5),
        (1, 0),
        (1, -1)
    ]
)
def test_product_list_invalid_pagination(
    auth_headers, page_num, page_size
):
    response = requests.get(
        f"{BASE_URL}/product/list",
        headers=auth_headers,
        params={
            "pageNum": page_num,
            "pageSize": page_size
        },
        timeout=10
    )

    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    data = result["data"]

    assert data["pageNum"] == page_num
    assert data["pageSize"] == page_size
    assert data["list"] == []

    # 检查当前接口对异常分页参数的处理
    if page_size <= 0:
        assert data["totalPage"] == 0
    else:
        assert isinstance(data["totalPage"], int)
        assert data["totalPage"] >= 0


def test_product_update_info_success(auth_headers):
    # 查询商品 ID 为 1 的商品编辑信息
    product_id = 1

    response = requests.get(
        f"{BASE_URL}/product/updateInfo/{product_id}",
        headers=auth_headers,
        timeout=10
    )

    # 验证 HTTP 状态码
    assert response.status_code == 200

    # 验证业务状态码
    result = response.json()
    assert result["code"] == 200
    assert result["message"] == "操作成功"

    # 验证商品信息
    data = result["data"]

    assert data["id"] == product_id
    assert isinstance(data["name"], str)
    assert data["name"] != ""
    assert isinstance(data["price"], (int, float))
    assert data["price"] >= 0
    assert isinstance(data["stock"], int)
    assert data["stock"] >= 0

    # 验证商品属性列表
    assert isinstance(data["productAttributeValueList"], list)



@pytest.mark.parametrize(
    "product_id",
    [
        99999999,
        0,
        -1
    ]
)
def test_product_update_info_invalid_id(auth_headers, product_id):
    # 测试不存在的商品 ID 和异常边界值
    response = requests.get(
        f"{BASE_URL}/product/updateInfo/{product_id}",
        headers=auth_headers,
        timeout=10
    )

    # 验证 HTTP 状态码
    assert response.status_code == 200

    result = response.json()

    # 验证接口当前的实际响应
    assert result["code"] == 200
    assert result["message"] == "操作成功"
    assert result["data"] is None


def test_product_update_info_invalid_type(auth_headers):
    # 商品 ID 使用非数字字符串
    response = requests.get(
        f"{BASE_URL}/product/updateInfo/abc",
        headers=auth_headers,
        timeout=10
    )

    # 验证当前接口的实际响应
    assert response.status_code == 400

    result = response.json()

    assert result["code"] == 401
    assert "暂未登录" in result["message"]
