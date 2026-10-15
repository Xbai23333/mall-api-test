
from api.base_api import BaseApi


class LoginApi(BaseApi):

    def login(self, username, password):
        return self.post(
            "/admin/login",
            json={
                "username": username,
                "password": password
            }
        )
