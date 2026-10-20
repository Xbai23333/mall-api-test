
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


# Allure 测试用例中文标题映射
ALLURE_TEST_TITLES = {
    # 断言工具模块
    "test_assert_api_response_success": "正常接口响应断言成功",
    "test_assert_api_response_wrong_http_status": "HTTP状态码错误时断言失败",
    "test_assert_api_response_wrong_business_code": "业务状态码错误时断言失败",
    "test_assert_api_response_custom_expected_code": "自定义业务状态码断言成功",

    # 商品分类模块
    "test_category_list_success": "查询商品分类列表成功",
    "test_category_list_page_two": "查询商品分类列表第二页",
    "test_category_list_children_success": "查询子分类列表成功",
    "test_category_list_without_token": "未登录查询商品分类列表",
    "test_category_list_nonexistent_parent": "查询不存在的父分类",
    "test_category_detail_success": "查询商品分类详情成功",
    "test_category_list_invalid_pagination": "商品分类列表分页参数异常",
    "test_category_list_negative_parent_id": "使用负数父分类ID查询",
    "test_category_detail_nonexistent_id": "查询不存在的商品分类详情",
    "test_category_list_invalid_parent_id_type": "父分类ID类型错误",

    # 商品模块
    "test_product_list_success": "查询商品列表成功",
    "test_product_list_page_two": "查询商品列表第二页",
    "test_product_list_search_keyword": "根据关键词搜索商品",
    "test_product_list_without_token": "未登录查询商品列表",
    "test_product_list_invalid_pagination": "商品列表分页参数异常",
    "test_product_update_info_success": "修改商品信息成功",
    "test_product_update_info_invalid_id": "修改不存在的商品",
    "test_product_update_info_invalid_type": "修改商品时参数类型错误",

    # 订单模块
    "test_order_list_success": "查询订单列表成功",
    "test_order_list_page_two": "查询订单列表第二页",
    "test_order_list_without_token": "未登录查询订单列表",
    "test_order_detail_success": "查询订单详情成功",
    "test_order_list_filter_by_status": "根据订单状态筛选",
    "test_order_list_filter_multiple_status": "多种订单状态筛选",
    "test_order_list_filter_by_order_sn": "根据订单编号筛选",
    "test_order_list_nonexistent_order_sn": "查询不存在的订单编号",
    "test_order_detail_nonexistent_id": "查询不存在的订单详情",
    "test_order_detail_invalid_id_type": "订单ID类型错误",
}

def pytest_runtest_call(item):
    """在测试执行期间设置 Allure 中文标题。"""
    import allure

    if item.path.name == "test_login.py":
        return

    chinese_title = ALLURE_TEST_TITLES.get(item.originalname)

    if chinese_title:
        if hasattr(item, "callspec"):
            chinese_title = f"{chinese_title} [{item.callspec.id}]"

        allure.dynamic.title(chinese_title)
