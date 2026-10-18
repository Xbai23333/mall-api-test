
from api.base_api import BaseApi


class OrderApi(BaseApi):

    def get_order_list(
        self,
        headers=None,
        page_num=1,
        page_size=5,
        query_params=None
    ):
        params = {
            "pageNum": page_num,
            "pageSize": page_size
        }

        if query_params:
            params.update(query_params)

        return self.get(
            "/order/list",
            headers=headers,
            params=params
        )

    def get_order_detail(self, order_id, headers=None):
        return self.get(
            f"/order/{order_id}",
            headers=headers
        )
