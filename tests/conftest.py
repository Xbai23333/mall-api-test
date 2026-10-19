
import pytest
from api.login_api import LoginApi
from config.settings import TEST_USERNAME, TEST_PASSWORD
from utils.logger import logger


@pytest.fixture(scope="session")
def auth_headers():
    # 创建登录接口对象
    login_api = LoginApi()

    # 登录管理员账号，获取Token
    response = login_api.login(
        username=TEST_USERNAME,
        password=TEST_PASSWORD
    )

    # 验证登录请求成功
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    token = result["data"]["token"]
    token_head = result["data"]["tokenHead"]

    # 返回带有Token的请求头
    return {
        "Authorization": token_head + token
    }

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    记录测试执行结果，避免在日志中输出敏感信息。
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    if report.failed:
        error_type = (
            call.excinfo.typename
            if call.excinfo is not None
            else "UnknownError"
        )

        logger.error(
            "测试失败：%s | 异常类型=%s",
            item.nodeid,
            error_type
        )

    elif report.passed:
        logger.info(
            "测试通过：%s",
            item.nodeid
        )
