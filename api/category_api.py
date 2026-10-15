
from api.base_api import BaseApi


class CategoryApi(BaseApi):

    def get_category_list(
        self,
        parent_id,
        headers=None,
        page_num=1,
        page_size=5
    ):
        return self.get(
            f"/productCategory/list/{parent_id}",
            headers=headers,
            params={
                "pageNum": page_num,
                "pageSize": page_size
            }
        )

    def get_category_detail(self, category_id, headers=None):
        return self.get(
            f"/productCategory/{category_id}",
            headers=headers
        )
