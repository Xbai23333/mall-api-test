import allure
from decimal import Decimal

from api.product_api import ProductApi
from utils.db_utils import get_any_product

product_api = ProductApi()

@allure.epic("Mall 商城接口自动化测试")
@allure.feature("商品管理")
@allure.story("商品接口与数据库一致性校验")
@allure.title("商品详情接口数据与MySQL数据库一致")
def test_product_info_matches_database(auth_headers):
    # 1. 从数据库动态获取测试商品
    db_product = get_any_product()

    assert db_product is not None, "数据库中没有可用于测试的商品"

    product_id = db_product["id"]

    # 2. 根据数据库中的商品ID调用接口
    response = product_api.get_product_update_info(
        product_id=product_id,
        headers=auth_headers
    )

    # 3. 验证接口调用成功
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == 200

    api_product = result["data"]

    # 4. 比较接口数据与数据库数据
    assert api_product["id"] == db_product["id"]
    assert api_product["name"] == db_product["name"]

    # 使用Decimal比较价格，避免浮点数精度问题
    assert Decimal(str(api_product["price"])) == db_product["price"]

    assert api_product["stock"] == db_product["stock"]
