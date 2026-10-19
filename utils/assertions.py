
def assert_api_response(
    response,
    expected_http_status=200,
    expected_code=200
):
    """
    验证接口的HTTP状态码和业务状态码。

    参数：
    response：requests返回的响应对象
    expected_http_status：预期HTTP状态码
    expected_code：预期业务状态码

    返回：
    解析后的JSON响应数据
    """

    # 验证HTTP状态码
    assert response.status_code == expected_http_status, (
        f"HTTP状态码不符合预期："
        f"预期={expected_http_status}，"
        f"实际={response.status_code}"
    )

    # 解析JSON响应
    result = response.json()

    # 验证业务状态码
    actual_code = result.get("code")

    assert actual_code == expected_code, (
        f"业务状态码不符合预期："
        f"预期={expected_code}，"
        f"实际={actual_code}，"
        f"响应消息={result.get('message')}"
    )

    return result
