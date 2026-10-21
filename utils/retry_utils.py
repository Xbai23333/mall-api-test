from requests.exceptions import Timeout


def retry_on_timeout(func, *args, max_attempts=2, **kwargs):
    """
    通用超时重试函数。

    func: 需要调用的函数
    args: 位置参数
    max_attempts: 最大尝试次数，默认2次
    kwargs: 关键字参数
    """
    if max_attempts < 1:
        raise ValueError("max_attempts必须大于等于1")

    for attempt in range(max_attempts):
        try:
            return func(*args, **kwargs)

        except Timeout:
            if attempt == max_attempts - 1:
                raise