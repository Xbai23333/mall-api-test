import pytest
from api.order_api import OrderApi
from utils.data_loader import load_json_data


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
    "case",
    load_json_data("data/order_status.json"),
    ids=lambda case: case["case_id"]
)
def test_order_list_filter_multiple_status(
    auth_headers, case
):
    status = case["status"]

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

    for order in orders:
        assert order["status"] == status



def test_order_list_filter_by_order_sn(auth_headers):
    # 第一步：查询订单列表，获取真实订单编号
    list_response = order_api.get_order_list(
        headers=auth_headers,
        page_num=1,
        page_size=5
    )

    assert list_response.status_code == 200

    list_result = list_response.json()
    assert list_result["code"] == 200

    orders = list_result["data"]["list"]
    assert orders, "测试环境中没有可用订单"

    order_sn = orders[0]["orderSn"]
    assert order_sn, "订单编号不能为空"

    # 第二步：使用真实订单编号查询
    response = order_api.get_order_list(
        headers=auth_headers,
        page_num=1,
        page_size=10,
        query_params={
            "orderSn": order_sn
        }
    )

    # 第三步：验证查询结果
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    filtered_orders = result["data"]["list"]

    assert len(filtered_orders) > 0

    # 验证目标订单存在
    assert any(
        order["orderSn"] == order_sn
        for order in filtered_orders
    )

    # 验证所有返回订单编号完全匹配
    for order in filtered_orders:
        assert order["orderSn"] == order_sn


def test_order_list_nonexistent_order_sn(auth_headers):
    # 使用一个不存在的订单编号查询
    nonexistent_order_sn = "AUTO_TEST_NOT_EXIST_999999"

    response = order_api.get_order_list(
        headers=auth_headers,
        page_num=1,
        page_size=5,
        query_params={
            "orderSn": nonexistent_order_sn
        }
    )

    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    data = result["data"]

    assert isinstance(data["list"], list)
    assert data["list"] == []
    assert data["total"] == 0


@pytest.mark.parametrize(
    "order_id",
    [999999999, 0, -1]
)
def test_order_detail_nonexistent_id(
    auth_headers, order_id
):
    # 查询不存在或不合理的订单ID
    response = order_api.get_order_detail(
        order_id=order_id,
        headers=auth_headers
    )

    assert response.status_code == 200

    result = response.json()

    # 验证当前后端的实际行为
    assert result["code"] == 200
    assert result["data"] is None


def test_order_detail_invalid_id_type(auth_headers):
    # 使用非数字订单ID
    response = order_api.get_order_detail(
        order_id="abc",
        headers=auth_headers
    )

    assert response.status_code == 400

    result = response.json()

    # 当前后端返回401业务码，属于待修复问题
    assert result["code"] == 401
    assert "暂未登录" in result["message"]
