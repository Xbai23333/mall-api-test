import allure
import pytest

from api.product_api import ProductApi
from utils.db_utils import get_product_by_id

product_api = ProductApi()

@allure.feature("商品管理")
@allure.story("商品接口与数据库一致性校验")
@allure.title("商品详情接口数据与MySQL数据库一致")
def test_product_info_matches_database(auth_headers):
    # 1. 指定测试商品
    product_id = 1

    # 2. 调用商品接口
    response = product_api.get_product_update_info(
        product_id=product_id,
        headers=auth_headers
    )

    # 3. 验证接口调用成功
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    api_product = result["data"]

    # 4. 查询MySQL数据库
    db_product = get_product_by_id(product_id)

    assert db_product is not None, "数据库中不存在该商品"

    # 5. 比较接口数据与数据库数据
    assert api_product["id"] == db_product["id"]
    assert api_product["name"] == db_product["name"]

    # MySQL的DECIMAL字段会被PyMySQL转换为Decimal类型
    # 使用Decimal比较价格，避免浮点数精度问题
    from decimal import Decimal

    assert Decimal(str(api_product["price"])) == db_product["price"]

    assert api_product["stock"] == db_product["stock"]
