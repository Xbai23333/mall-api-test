
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("MALL_BASE_URL", "http://localhost:8080")

# 第一步：登录管理员账号
login_response = requests.post(
    f"{BASE_URL}/admin/login",
    json={
        "username": os.getenv("MALL_TEST_USERNAME"),
        "password": os.getenv("MALL_TEST_PASSWORD")
    },
    timeout=10
)

login_result = login_response.json()

assert login_response.status_code == 200
assert login_result["code"] == 200

token = login_result["data"]["token"]
token_head = login_result["data"]["tokenHead"]

# 第二步：携带 Token 请求非法商品 ID
response = requests.get(
    f"{BASE_URL}/product/updateInfo/abc",
    headers={
        "Authorization": token_head + token
    },
    timeout=10
)

# 第三步：打印响应结果
print("HTTP状态码：", response.status_code)
print("响应内容：", response.text)


# 第四步：使用同一个 Token 请求正常商品 ID
normal_response = requests.get(
    f"{BASE_URL}/product/updateInfo/1",
    headers={
        "Authorization": token_head + token
    },
    timeout=10
)

normal_result = normal_response.json()

print("正常商品HTTP状态码：", normal_response.status_code)
print("正常商品业务状态码：", normal_result.get("code"))
print("正常商品返回ID：",
      normal_result.get("data", {}).get("id")
      if isinstance(normal_result.get("data"), dict)
      else None)


# 第五步：检查 /error 路径是否受到认证限制

error_response = requests.get(
    f"{BASE_URL}/error",
    headers={
        "Authorization": token_head + token
    },
    timeout=10
)

print("/error HTTP状态码：", error_response.status_code)
print("/error 响应内容：", error_response.text)

