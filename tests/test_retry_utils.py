import pytest
from unittest.mock import Mock, patch, call
from requests.exceptions import Timeout, ConnectionError

from api.product_api import ProductApi
from utils.retry_utils import retry_on_timeout

def test_mock_product_list_retry_success():
    product_api = ProductApi()

    # 模拟第二次请求成功时的响应
    mock_response = Mock()
    mock_response.status_code = 200

    mock_response.json.return_value = {
        "code": 200,
        "message": "操作成功",
        "data": {
            "total": 1,
            "list": [
                {"id": 1, "name": "重试成功商品"}
            ]
        }
    }

    # 第一次请求超时，第二次返回成功响应
    with patch.object(
        product_api,
        "get",
        side_effect=[
            Timeout("第一次请求超时"),
            mock_response
        ]
    ) as mock_get:

        response = retry_on_timeout(
    product_api.get_product_list,
    headers={"Authorization": "mock-token"},
    page_num=1,
    page_size=5
)

        # 验证最终响应成功
        assert response.status_code == 200

        result = response.json()

        assert result["code"] == 200
        assert result["data"]["list"][0]["name"] == "重试成功商品"

        # 验证底层请求一共执行了2次
        assert mock_get.call_count == 2

def test_mock_product_list_retry_failed():
    product_api = ProductApi()

    # 模拟连续两次请求超时
    with patch.object(
        product_api,
        "get",
        side_effect=[
            Timeout("第一次请求超时"),
            Timeout("第二次请求超时")
        ]
    ) as mock_get:

        # 验证第二次超时后，程序向外抛出异常
        with pytest.raises(Timeout, match="第二次请求超时"):
            retry_on_timeout(
    product_api.get_product_list,
    headers={"Authorization": "mock-token"},
    page_num=1,
    page_size=5
)

        # 验证程序只尝试了2次
        assert mock_get.call_count == 2

@pytest.mark.parametrize(
    "max_attempts",
    [1, 2, 3],
    ids=["retry_1", "retry_2", "retry_3"]
)
def test_retry_max_attempts(max_attempts):
    # 创建模拟函数
    mock_func = Mock(
        side_effect=Timeout("模拟请求超时")
    )

    # 验证最终抛出超时异常
    with pytest.raises(Timeout, match="模拟请求超时"):
        retry_on_timeout(
            mock_func,
            max_attempts=max_attempts
        )

    # 验证实际调用次数
    assert mock_func.call_count == max_attempts

def test_retry_invalid_max_attempts():
    mock_func = Mock()

    # max_attempts=0属于非法参数
    with pytest.raises(
        ValueError,
        match="max_attempts必须大于等于1"
    ):
        retry_on_timeout(
            mock_func,
            max_attempts=0
        )

    # 参数非法时，不应该执行请求
    mock_func.assert_not_called()

@pytest.mark.parametrize(
    "success_attempt",
    [1, 2, 3],
    ids=["success_first", "success_second", "success_third"]
)
def test_retry_success_at_different_attempts(success_attempt):
    # 模拟成功时返回的数据
    expected_result = {"code": 200, "message": "请求成功"}

    # 前几次超时，最后一次成功
    side_effects = [
        Timeout("模拟请求超时")
        for _ in range(success_attempt - 1)
    ]
    side_effects.append(expected_result)

    # 创建模拟函数
    mock_func = Mock(side_effect=side_effects)

    # 最多允许尝试3次
    result = retry_on_timeout(
        mock_func,
        max_attempts=3
    )

    # 验证返回结果
    assert result == expected_result

    # 验证成功后立即停止，不再多次调用
    assert mock_func.call_count == success_attempt

def test_retry_connection_error_no_retry():
    # 1. 创建模拟函数，调用时抛出连接失败异常
    mock_func = Mock(
        side_effect=ConnectionError("模拟连接失败")
    )

    # 2. 验证程序直接抛出ConnectionError
    with pytest.raises(
        ConnectionError,
        match="模拟连接失败"
    ):
        retry_on_timeout(
            mock_func,
            max_attempts=3
        )

    # 3. 验证只调用了一次，没有重试
    mock_func.assert_called_once()

def test_retry_args_and_kwargs():
    # 1. 创建模拟函数
    mock_func = Mock(return_value="请求成功")

    # 2. 调用通用重试工具
    result = retry_on_timeout(
        mock_func,
        100,
        "商品A",
        page_num=1,
        page_size=5,
        max_attempts=2
    )

    # 3. 验证返回结果
    assert result == "请求成功"

    # 4. 验证原始函数收到的参数
    mock_func.assert_called_once_with(
        100,
        "商品A",
        page_num=1,
        page_size=5
    )

def test_retry_each_call_has_correct_args():
    # 1. 创建模拟函数
    mock_func = Mock(
        side_effect=[
            Timeout("第一次请求超时"),
            "第二次请求成功"
        ]
    )

    # 2. 执行重试函数
    result = retry_on_timeout(
        mock_func,
        100,
        page_num=1,
        page_size=5,
        max_attempts=3
    )

    # 3. 验证最终结果
    assert result == "第二次请求成功"

    # 4. 验证两次调用的参数
    expected_calls = [
        call(100, page_num=1, page_size=5),
        call(100, page_num=1, page_size=5)
    ]

    mock_func.assert_has_calls(expected_calls)

    # 5. 验证一共只调用了2次
    assert mock_func.call_count == 2