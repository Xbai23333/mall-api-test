
import requests
from config.settings import BASE_URL, REQUEST_TIMEOUT


class BaseApi:

    def __init__(self):
        self.base_url = BASE_URL

    def get(self, path, headers=None, params=None):
        return requests.get(
            f"{self.base_url}{path}",
            headers=headers,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

    def post(self, path, headers=None, json=None):
        return requests.post(
            f"{self.base_url}{path}",
            headers=headers,
            json=json,
            timeout=REQUEST_TIMEOUT
        )
