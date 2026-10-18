
from api.login_api import LoginApi
from api.order_api import OrderApi
from config.settings import TEST_USERNAME, TEST_PASSWORD


# 第一步：管理员登录
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


# 第二步：按订单状态筛选
order_api = OrderApi()

response = order_api.get_order_list(
    headers=headers,
    page_num=1,
    page_size=10,
    query_params={
        "status": 4
    }
)

print("HTTP状态码：", response.status_code)

result = response.json()

print("业务状态码：", result.get("code"))
print("响应消息：", result.get("message"))

data = result.get("data")

if isinstance(data, dict):
    orders = data.get("list", [])

    print("订单总数：", data.get("total"))
    print("当前页订单数量：", len(orders))

    statuses = [order.get("status") for order in orders]

    print("返回的订单状态：", statuses)

    if orders:
        print("是否全部为状态4：", all(status == 4 for status in statuses))
else:
    print("data类型：", type(data).__name__)
