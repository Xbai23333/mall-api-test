
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("MALL_BASE_URL", "http://localhost:8080")


def test_category_list_success(auth_headers):
    # 第一步：查询一级商品分类
    response = requests.get(
        f"{BASE_URL}/productCategory/list/0",
        headers=auth_headers,
        params={
            "pageNum": 1,
            "pageSize": 5
        },
        timeout=10
    )

    # 第二步：验证 HTTP 状态码
    assert response.status_code == 200

    # 第三步：验证业务状态码
    result = response.json()
    assert result["code"] == 200
    assert result["message"] == "操作成功"

    # 第四步：验证分页信息
    data = result["data"]

    assert data["pageNum"] == 1
    assert data["pageSize"] == 5
    assert isinstance(data["list"], list)
    assert len(data["list"]) <= 5
    assert data["total"] >= len(data["list"])

    # 第五步：验证商品分类信息
    assert len(data["list"]) > 0

    for category in data["list"]:
        assert category["parentId"] == 0
        assert isinstance(category["id"], int)
        assert isinstance(category["name"], str)
        assert category["name"] != ""


def test_category_list_page_two(auth_headers):
    # 第一步：查询一级商品分类的第二页
    response = requests.get(
        f"{BASE_URL}/productCategory/list/0",
        headers=auth_headers,
        params={
            "pageNum": 2,
            "pageSize": 5
        },
        timeout=10
    )

    # 第二步：验证请求成功
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    # 第三步：验证分页信息
    data = result["data"]

    assert data["pageNum"] == 2
    assert data["pageSize"] == 5
    assert isinstance(data["list"], list)
    assert len(data["list"]) <= 5

    # 第四步：根据总数检查第二页的数据量
    if data["total"] > 5:
        assert len(data["list"]) == min(
            data["total"] - 5, 5
        )

    # 第五步：验证分类属于一级分类
    for category in data["list"]:
        assert category["parentId"] == 0


def test_category_list_children_success(auth_headers):
    # 第一步：查询服装分类下面的子分类
    parent_id = 1

    response = requests.get(
        f"{BASE_URL}/productCategory/list/{parent_id}",
        headers=auth_headers,
        params={
            "pageNum": 1,
            "pageSize": 5
        },
        timeout=10
    )

    # 第二步：验证请求成功
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200
    assert result["message"] == "操作成功"

    # 第三步：验证分页信息
    data = result["data"]

    assert data["pageNum"] == 1
    assert data["pageSize"] == 5
    assert isinstance(data["list"], list)
    assert len(data["list"]) <= 5
    assert data["total"] >= len(data["list"])

    # 第四步：验证返回的是服装的子分类
    assert len(data["list"]) > 0

    for category in data["list"]:
        assert category["parentId"] == parent_id
        assert category["level"] == 1
        assert isinstance(category["name"], str)
        assert category["name"] != ""
