
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class BaseApi:
    def __init__(self):
        self.base_url = os.getenv(
            "MALL_BASE_URL",
            "http://localhost:8080"
        ).rstrip("/")

    def get(self, path, headers=None, params=None):
        return requests.get(
            f"{self.base_url}{path}",
            headers=headers,
            params=params,
            timeout=10
        )

    def post(self, path, headers=None, json=None):
        return requests.post(
            f"{self.base_url}{path}",
            headers=headers,
            json=json,
            timeout=10
        )
