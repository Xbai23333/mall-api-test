
from api.login_api import LoginApi
from api.order_api import OrderApi
from config.settings import TEST_USERNAME, TEST_PASSWORD


# 第一步：登录管理员账号
login_api = LoginApi()

login_response = login_api.login(
    username=TEST_USERNAME,
    password=TEST_PASSWORD
)

assert login_response.status_code == 200
login_result = login_response.json()
assert login_result["code"] == 200

token = login_result["data"]["token"]
token_head = login_result["data"]["tokenHead"]

headers = {
    "Authorization": token_head + token
}


# 第二步：获取真实订单编号
order_api = OrderApi()

list_response = order_api.get_order_list(
    headers=headers,
    page_num=1,
    page_size=5
)

assert list_response.status_code == 200
list_result = list_response.json()
assert list_result["code"] == 200

orders = list_result["data"]["list"]
assert orders, "当前测试环境没有可用订单"

order_sn = orders[0]["orderSn"]

print("已获取一条真实订单编号")
print("订单编号是否为空：", bool(order_sn))


# 第三步：根据订单编号筛选
response = order_api.get_order_list(
    headers=headers,
    page_num=1,
    page_size=10,
    query_params={
        "orderSn": order_sn
    }
)

print("HTTP状态码：", response.status_code)

result = response.json()

print("业务状态码：", result.get("code"))
print("响应消息：", result.get("message"))

data = result.get("data")

if isinstance(data, dict):
    filtered_orders = data.get("list", [])

    print("筛选结果数量：", len(filtered_orders))

    print(
        "是否包含目标订单：",
        any(
            order.get("orderSn") == order_sn
            for order in filtered_orders
        )
    )

    print(
        "是否全部匹配订单编号：",
        bool(filtered_orders) and all(
            order.get("orderSn") == order_sn
            for order in filtered_orders
        )
    )
else:
    print("data类型：", type(data).__name__)
