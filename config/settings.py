
import os
from dotenv import load_dotenv


# 加载项目根目录下的 .env 文件
load_dotenv()


# Mall 后端地址
BASE_URL = os.getenv(
    "MALL_BASE_URL",
    "http://localhost:8080"
).rstrip("/")


# 测试管理员账号
TEST_USERNAME = os.getenv("MALL_TEST_USERNAME")


# 测试管理员密码
TEST_PASSWORD = os.getenv("MALL_TEST_PASSWORD")


# HTTP 请求超时时间（秒）
REQUEST_TIMEOUT = 10
