
from api.login_api import LoginApi
from api.base_api import BaseApi
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


# 第二步：查询第一页订单
api = BaseApi()

response = api.get(
    "/order/list",
    headers=headers,
    params={
        "pageNum": 1,
        "pageSize": 5
    }
)


# 第三步：查看返回结果
print("HTTP状态码：", response.status_code)

result = response.json()

print("业务状态码：", result.get("code"))
print("响应消息：", result.get("message"))

data = result.get("data")

if isinstance(data, dict):
    print("data字段：", list(data.keys()))

    orders = data.get("list")

    if isinstance(orders, list):
        print("当前页订单数量：", len(orders))
        print("订单总数：", data.get("total"))

        if orders:
            print("第一条订单ID：", orders[0].get("id"))
            print("第一条订单状态：", orders[0].get("status"))
else:
    print("data类型：", type(data).__name__)
