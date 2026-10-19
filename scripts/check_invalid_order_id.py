
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


# 第二步：创建订单API对象
order_api = OrderApi()


# 第三步：测试不同的异常订单ID
invalid_ids = [
    999999999,
    0,
    -1,
    "abc"
]

for order_id in invalid_ids:
    print("\n==============================")
    print("测试订单ID：", order_id)

    response = order_api.get_order_detail(
        order_id=order_id,
        headers=headers
    )

    print("HTTP状态码：", response.status_code)

    try:
        result = response.json()

        print("业务状态码：", result.get("code"))
        print("响应消息：", result.get("message"))

        data = result.get("data")

        # 避免输出订单详情中的个人信息
        if data is None:
            print("data：None")
        else:
            print("data类型：", type(data).__name__)

    except ValueError:
        print("响应不是JSON格式")
        print("响应内容长度：", len(response.text))
