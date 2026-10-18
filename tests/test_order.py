import pytest
from api.order_api import OrderApi


order_api = OrderApi()


def test_order_list_success(auth_headers):
    # 查询第一页订单，每页5条
    response = order_api.get_order_list(
        headers=auth_headers,
        page_num=1,
        page_size=5
    )

    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    data = result["data"]

    assert data["pageNum"] == 1
    assert data["pageSize"] == 5
    assert isinstance(data["list"], list)
    assert len(data["list"]) <= 5
    assert data["total"] >= len(data["list"])


def test_order_list_page_two(auth_headers):
    # 查询第二页，每页3条订单
    response = order_api.get_order_list(
        headers=auth_headers,
        page_num=2,
        page_size=3
    )

    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    data = result["data"]

    assert data["pageNum"] == 2
    assert data["pageSize"] == 3
    assert isinstance(data["list"], list)
    assert len(data["list"]) <= 3


def test_order_list_without_token():
    # 不携带Token访问订单列表
    response = order_api.get_order_list(
        headers=None,
        page_num=1,
        page_size=5
    )

    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 401
    assert "暂未登录" in result["message"]


def test_order_detail_success(auth_headers):
    # 先查询订单列表，动态获取真实订单ID
    list_response = order_api.get_order_list(
        headers=auth_headers,
        page_num=1,
        page_size=5
    )

    assert list_response.status_code == 200

    list_result = list_response.json()
    assert list_result["code"] == 200

    orders = list_result["data"]["list"]

    assert len(orders) > 0, "测试环境中没有可用订单"

    order_id = orders[0]["id"]

    # 再根据真实订单ID查询详情
    response = order_api.get_order_detail(
        order_id=order_id,
        headers=auth_headers
    )

    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    data = result["data"]

    assert isinstance(data, dict)
    assert data["id"] == order_id


def test_order_list_filter_by_status(auth_headers):
    # 按订单状态4筛选
    response = order_api.get_order_list(
        headers=auth_headers,
        page_num=1,
        page_size=10,
        query_params={
            "status": 4
        }
    )

    # 验证HTTP和业务状态码
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    data = result["data"]
    orders = data["list"]

    # 验证分页结果
    assert data["pageNum"] == 1
    assert data["pageSize"] == 10
    assert isinstance(orders, list)
    assert len(orders) <= 10
    assert data["total"] >= len(orders)

    # 验证返回的订单状态全部为4
    for order in orders:
        assert order["status"] == 4


@pytest.mark.parametrize(
    "status",
    [0, 1, 2, 3, 4]
)
def test_order_list_filter_multiple_status(
    auth_headers, status
):
    # 按不同订单状态查询
    response = order_api.get_order_list(
        headers=auth_headers,
        page_num=1,
        page_size=10,
        query_params={
            "status": status
        }
    )

    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    data = result["data"]
    orders = data["list"]

    assert isinstance(orders, list)
    assert len(orders) <= 10

    # 验证订单状态与查询条件一致
    for order in orders:
        assert order["status"] == status
