
from api.base_api import BaseApi


class ProductApi(BaseApi):

    def get_product_list(
        self,
        headers=None,
        page_num=1,
        page_size=5,
        keyword=None
    ):
        params = {
            "pageNum": page_num,
            "pageSize": page_size
        }

        if keyword is not None:
            params["keyword"] = keyword

        return self.get(
            "/product/list",
            headers=headers,
            params=params
        )

    def get_product_update_info(
        self,
        product_id,
        headers=None
    ):
        return self.get(
            f"/product/updateInfo/{product_id}",
            headers=headers
        )
