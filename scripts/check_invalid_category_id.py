
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv(
    "MALL_BASE_URL",
    "http://localhost:8080"
).rstrip("/")

username = os.getenv("MALL_TEST_USERNAME")
password = os.getenv("MALL_TEST_PASSWORD")

# 检查测试账号是否已配置
if not username or not password:
    raise ValueError("请检查.env中的测试账号和密码配置")

# 第一步：登录获取Token
login_response = requests.post(
    f"{BASE_URL}/admin/login",
    json={
        "username": username,
        "password": password
    },
    timeout=10
)

print("登录HTTP状态码：", login_response.status_code)

if login_response.status_code != 200:
    raise RuntimeError(
        f"登录请求失败，HTTP状态码：{login_response.status_code}"
    )

login_result = login_response.json()

if login_result["code"] != 200:
    raise RuntimeError(
        f"登录业务失败：{login_result.get('message')}"
    )

token = login_result["data"]["token"]
token_head = login_result["data"]["tokenHead"]

headers = {
    "Authorization": token_head + token
}

# 第二步：请求非法分类ID
response = requests.get(
    f"{BASE_URL}/productCategory/list/abc",
    headers=headers,
    params={
        "pageNum": 1,
        "pageSize": 5
    },
    timeout=10
)

# 第三步：输出测试结果
print("分类接口HTTP状态码：", response.status_code)
print("分类接口响应内容：", response.text)
