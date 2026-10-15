
import pytest
from api.category_api import CategoryApi


# 创建商品分类接口对象
category_api = CategoryApi()


def test_category_list_success(auth_headers):
    # 第一步：查询一级商品分类
    response = category_api.get_category_list(
        parent_id=0,
        headers=auth_headers,
        page_num=1,
        page_size=5
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
    response = category_api.get_category_list(
        parent_id=0,
        headers=auth_headers,
        page_num=2,
        page_size=5
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

    response = category_api.get_category_list(
        parent_id=parent_id,
        headers=auth_headers,
        page_num=1,
        page_size=5
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


def test_category_list_without_token():
    # 第一步：不携带Token查询商品分类
    response = category_api.get_category_list(
        parent_id=0,
        headers=None
    )

    # 第二步：验证接口的权限控制
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 401
    assert "暂未登录" in result["message"]


def test_category_list_nonexistent_parent(auth_headers):
    # 第一步：查询不存在的父分类
    parent_id = 99999999

    response = category_api.get_category_list(
        parent_id=parent_id,
        headers=auth_headers,
        page_num=1,
        page_size=5
    )

    # 第二步：验证请求结果
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200
    assert result["message"] == "操作成功"

    # 第三步：验证返回空列表
    data = result["data"]

    assert data["pageNum"] == 1
    assert data["pageSize"] == 5
    assert data["total"] == 0
    assert data["totalPage"] == 0
    assert data["list"] == []


def test_category_detail_success(auth_headers):
    # 第一步：查询ID为7的商品分类详情
    category_id = 7

    response = category_api.get_category_detail(
        category_id=category_id,
        headers=auth_headers
    )

    # 第二步：验证请求成功
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200
    assert result["message"] == "操作成功"

    # 第三步：验证分类详情
    data = result["data"]

    assert data["id"] == category_id
    assert data["parentId"] == 1
    assert data["name"] == "外套"
    assert data["level"] == 1

    # 第四步：验证分类信息类型
    assert isinstance(data["productCount"], int)
    assert isinstance(data["productUnit"], str)
    assert isinstance(data["keywords"], str)


@pytest.mark.parametrize(
    "page_num, page_size",
    [
        (0, 5),
        (1, 0)
    ]
)
def test_category_list_invalid_pagination(
    auth_headers, page_num, page_size
):
    # 第一步：使用非法分页参数查询商品分类
    response = category_api.get_category_list(
        parent_id=0,
        headers=auth_headers,
        page_num=page_num,
        page_size=page_size
    )

    # 第二步：验证HTTP状态码
    assert response.status_code == 200

    # 第三步：验证接口当前的业务响应
    result = response.json()

    assert result["code"] == 200
    assert result["message"] == "操作成功"

    # 第四步：验证分页信息
    data = result["data"]

    assert data["pageNum"] == page_num
    assert data["pageSize"] == page_size
    assert data["list"] == []

    # 第五步：验证返回的总数和总页数
    assert isinstance(data["total"], int)
    assert data["total"] >= 0

    if page_size == 0:
        assert data["totalPage"] == 0
    else:
        assert isinstance(data["totalPage"], int)
        assert data["totalPage"] >= 0


def test_category_list_negative_parent_id(auth_headers):
    # 使用负数父分类ID查询商品分类
    response = category_api.get_category_list(
        parent_id=-1,
        headers=auth_headers,
        page_num=1,
        page_size=5
    )

    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200
    assert result["message"] == "操作成功"

    data = result["data"]
    assert data["pageNum"] == 1
    assert data["pageSize"] == 5
    assert data["total"] == 0
    assert data["totalPage"] == 0
    assert data["list"] == []


def test_category_detail_nonexistent_id(auth_headers):
    # 查询不存在的商品分类详情
    response = category_api.get_category_detail(
        category_id=99999999,
        headers=auth_headers
    )

    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200
    assert result["message"] == "操作成功"
    assert result["data"] is None


def test_category_list_invalid_parent_id_type(auth_headers):
    # 使用非整数类型的父分类ID
    response = category_api.get_category_list(
        parent_id="abc",
        headers=auth_headers,
        page_num=1,
        page_size=5
    )

    # 验证当前接口实际返回的HTTP状态码
    assert response.status_code == 400

    result = response.json()

    # 记录当前接口的异常响应行为
    assert result["code"] == 401
    assert result["message"] == "暂未登录或token已经过期"
    assert "Full authentication is required" in result["data"]
