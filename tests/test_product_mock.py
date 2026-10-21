import pytest
from unittest.mock import Mock, patch
from requests.exceptions import Timeout, ConnectionError

from api.product_api import ProductApi


def test_mock_api_response():
    mock_response = Mock()
    mock_response.status_code = 200

    mock_response.json.return_value = {
        "code": 200,
        "message": "操作成功",
        "data": {
            "id": 1,
            "name": "测试商品"
        }
    }

    result = mock_response.json()

    assert mock_response.status_code == 200
    assert result["code"] == 200
    assert result["data"]["name"] == "测试商品"


def test_mock_product_list():
    product_api = ProductApi()

    mock_response = Mock()
    mock_response.status_code = 200

    mock_response.json.return_value = {
        "code": 200,
        "message": "操作成功",
        "data": {
            "pageNum": 1,
            "pageSize": 5,
            "total": 1,
            "list": [
                {"id": 1, "name": "Mock测试商品"}
            ]
        }
    }

    with patch.object(
        product_api,
        "get",
        return_value=mock_response
    ) as mock_get:

        response = product_api.get_product_list(
            headers={"Authorization": "mock-token"},
            page_num=1,
            page_size=5
        )

        assert response.status_code == 200

        result = response.json()

        assert result["code"] == 200
        assert result["data"]["total"] == 1
        assert result["data"]["list"][0]["name"] == "Mock测试商品"

        mock_get.assert_called_once_with(
            "/product/list",
            headers={"Authorization": "mock-token"},
            params={
                "pageNum": 1,
                "pageSize": 5
            }
        )


def test_mock_product_list_timeout():
    product_api = ProductApi()

    with patch.object(
        product_api,
        "get",
        side_effect=Timeout("模拟请求超时")
    ) as mock_get:

        with pytest.raises(Timeout, match="模拟请求超时"):
            product_api.get_product_list(
                headers={"Authorization": "mock-token"},
                page_num=1,
                page_size=5
            )

        mock_get.assert_called_once()


@pytest.mark.parametrize(
    "exception",
    [
        Timeout("模拟请求超时"),
        ConnectionError("模拟连接失败")
    ],
    ids=["timeout", "connection_error"]
)
def test_mock_product_list_network_error(exception):
    product_api = ProductApi()

    with patch.object(
        product_api,
        "get",
        side_effect=exception
    ) as mock_get:

        with pytest.raises(type(exception), match=str(exception)):
            product_api.get_product_list(
                headers={"Authorization": "mock-token"},
                page_num=1,
                page_size=5
            )

        mock_get.assert_called_once()