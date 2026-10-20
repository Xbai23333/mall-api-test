
import pytest
import allure
from unittest.mock import Mock
from utils.assertions import assert_api_response

pytestmark = [
    allure.epic("Mall 商城接口自动化测试"),
    allure.feature("断言工具单元测试"),
]

def test_assert_api_response_success():
    # 模拟一个正常的接口响应
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "code": 200,
        "message": "操作成功",
        "data": {"id": 1}
    }

    result = assert_api_response(response)

    assert result["data"]["id"] == 1


def test_assert_api_response_wrong_http_status():
    # 模拟HTTP状态码不正确
    response = Mock()
    response.status_code = 500

    with pytest.raises(
        AssertionError,
        match="HTTP状态码不符合预期"
    ):
        assert_api_response(response)


def test_assert_api_response_wrong_business_code():
    # 模拟业务状态码不正确
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "code": 500,
        "message": "操作失败",
        "data": None
    }

    with pytest.raises(
        AssertionError,
        match="业务状态码不符合预期"
    ):
        assert_api_response(response)


def test_assert_api_response_custom_expected_code():
    # 验证可以传入自定义预期业务状态码
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "code": 404,
        "message": "用户名或密码错误",
        "data": None
    }

    result = assert_api_response(
        response,
        expected_code=404
    )

    assert result["code"] == 404
