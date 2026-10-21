
import pytest
import allure
from api.product_api import ProductApi
from utils.assertions import assert_api_response
from utils.data_loader import load_json_data

# 创建商品接口对象
product_api = ProductApi()
pytestmark = [
    allure.epic("Mall 商城接口自动化测试"),
    allure.feature("商品模块"),
]

@pytest.mark.parametrize(
    "case",
    load_json_data("data/product_pagination.json"),
    ids=lambda case: case["case_id"]
)
def test_product_list_pagination(auth_headers, case):
    # 1. 读取JSON测试数据
    page_num = case["page_num"]
    page_size = case["page_size"]

    # 2. 调用商品列表接口
    response = product_api.get_product_list(
        headers=auth_headers,
        page_num=page_num,
        page_size=page_size
    )

    # 3. 验证接口响应
    result = assert_api_response(response)
    data = result["data"]

    # 4. 验证分页参数
    assert data["pageNum"] == page_num
    assert data["pageSize"] == page_size

    # 5. 验证商品列表
    assert isinstance(data["list"], list)
    assert len(data["list"]) <= page_size
    assert data["total"] >= len(data["list"])

    # 6. 验证当前页商品ID没有重复
    product_ids = [product["id"] for product in data["list"]]
    assert len(product_ids) == len(set(product_ids))

    # 7. 商品数量足够时，验证当前页返回完整数量
    if data["total"] >= page_num * page_size:
        assert len(data["list"]) == page_size


def test_product_list_search_keyword(auth_headers):
    # 按关键词查询商品
    response = product_api.get_product_list(
        headers=auth_headers,
        page_num=1,
        page_size=10,
        keyword="华为"
    )

    result = assert_api_response(response)

    products = result["data"]["list"]

    assert isinstance(products, list)
    assert len(products) > 0

    for product in products:
        assert "华为" in product["name"]


def test_product_list_without_token():
    # 不携带Token，直接请求商品列表
    response = product_api.get_product_list(
        headers=None,
        page_num=1,
        page_size=5
    )

    result = assert_api_response(
    response,
    expected_code=401
)

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
    # 使用非法分页参数查询商品
    response = product_api.get_product_list(
        headers=auth_headers,
        page_num=page_num,
        page_size=page_size
    )

    result = assert_api_response(response)

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
    # 查询商品ID为1的商品编辑信息
    product_id = 1

    response = product_api.get_product_update_info(
        product_id=product_id,
        headers=auth_headers
    )

    # 验证HTTP状态码
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
def test_product_update_info_invalid_id(
    auth_headers, product_id
):
    # 测试不存在的商品ID和异常边界值
    response = product_api.get_product_update_info(
        product_id=product_id,
        headers=auth_headers
    )

    # 验证HTTP状态码
    assert response.status_code == 200

    result = response.json()

    # 验证接口当前的实际响应
    assert result["code"] == 200
    assert result["message"] == "操作成功"
    assert result["data"] is None


def test_product_update_info_invalid_type(auth_headers):
    # 商品ID使用非数字字符串
    response = product_api.get_product_update_info(
        product_id="abc",
        headers=auth_headers
    )

    result = assert_api_response(
    response,
    expected_http_status=400,
    expected_code=401
)

    assert "暂未登录" in result["message"]
