import time
import requests

from config.settings import BASE_URL, REQUEST_TIMEOUT
from utils.logger import logger


class BaseApi:

    def __init__(self):
        self.base_url = BASE_URL

    def _request(self, method, path, headers=None, params=None, json=None):
        """
        统一发送HTTP请求，并记录请求日志。
        不记录请求头、请求体或响应体，避免泄露Token和密码。
        """
        url = f"{self.base_url}{path}"

        logger.info("开始请求：%s %s", method, url)

        start_time = time.perf_counter()

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
                timeout=REQUEST_TIMEOUT
            )

            elapsed = time.perf_counter() - start_time

            logger.info(
                "请求完成：%s %s | HTTP状态码=%s | 耗时=%.3f秒",
                method,
                url,
                response.status_code,
                elapsed
            )

            return response

        except requests.RequestException as error:
            elapsed = time.perf_counter() - start_time

            logger.error(
                "请求失败：%s %s | 耗时=%.3f秒 | 异常类型=%s",
                method,
                url,
                elapsed,
                type(error).__name__
            )

            raise

    def get(self, path, headers=None, params=None):
        return self._request(
            method="GET",
            path=path,
            headers=headers,
            params=params
        )

    def post(self, path, headers=None, json=None):
        return self._request(
            method="POST",
            path=path,
            headers=headers,
            json=json
        )