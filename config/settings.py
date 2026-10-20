
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
# MySQL 数据库配置
DB_HOST = os.getenv("MALL_DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("MALL_DB_PORT", "3306"))
DB_NAME = os.getenv("MALL_DB_NAME", "mall")
DB_USER = os.getenv("MALL_DB_USER")
DB_PASSWORD = os.getenv("MALL_DB_PASSWORD")
