# Mall 商城接口自动化测试项目

## 一、项目简介

本项目基于 GitHub 开源商城系统 Mall，使用 Python、pytest 和 requests 对商城后台管理系统进行接口自动化测试。

通过编写测试用例、执行接口请求、验证响应结果和生成 HTML 测试报告，实现对商城接口的自动化验证。

## 二、技术栈

- 后端项目：Java、Spring Boot、MySQL、Redis
- 接口测试：Swagger、Python、requests
- 自动化测试框架：pytest
- 测试报告：pytest-html
- 版本管理：Git、GitHub

## 三、已完成的测试内容

### 管理员登录接口

接口地址：`POST /admin/login`

| 用例编号 | 测试场景 | 测试结果 |
|---|---|---|
| TC_LOGIN_001 | 正确用户名和密码 | PASS |
| TC_LOGIN_002 | 错误密码 | PASS |
| TC_LOGIN_003 | 不存在的用户名 | PASS |
| TC_LOGIN_004 | 密码为空 | PASS |
| TC_LOGIN_005 | 用户名为空 | PASS |
| TC_LOGIN_006 | 用户名和密码同时为空 | PASS |

目前已完成6个登录接口自动化测试用例，最近一次执行全部通过。

### 商品列表接口

接口地址：`GET /product/list`

| 用例编号 | 测试场景 | 测试结果 |
|---|---|---|
| TC_PRODUCT_001 | 正常查询商品列表 | PASS |
| TC_PRODUCT_002 | 商品列表分页查询 | PASS |
| TC_PRODUCT_003 | 商品关键词搜索 | PASS |
| TC_PRODUCT_004 | 未登录访问商品列表 | PASS |

目前已完成4条商品列表接口自动化测试用例。

项目累计完成10条自动化测试用例，最近一次执行全部通过，通过率为100%。

商品接口测试使用 pytest fixture 复用管理员登录认证逻辑，减少重复代码，提高测试代码的可维护性。

## 四、项目目录

```text
mall-api-test/
├── tests/
│   ├── test_login.py
│   └── test_product.py
├── reports/
│   ├── login_report.html
│   └── report.html
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 五、运行方法
### 环境配置

本项目使用 `.env` 文件管理接口地址和测试账号，避免将敏感信息直接写入测试代码。

首次运行时，需要将 `.env.example` 复制为 `.env`，并根据本地测试环境填写对应配置：

```env
MALL_BASE_URL=http://localhost:8080
MALL_TEST_USERNAME=admin
MALL_TEST_PASSWORD=your_password_here
```

其中，`MALL_TEST_PASSWORD` 需要替换为本地测试账号的实际密码。

`.env` 文件已加入 `.gitignore`，不会被提交到 GitHub。请勿将真实密码或访问令牌写入公开文件。

1. 启动 Mall 商城后台及其依赖服务。
2. 安装 Python 项目依赖：

   `python -m pip install -r requirements.txt`

3. 执行自动化测试：

   `python -m pytest tests/ -v`

4. 生成 HTML 测试报告：

   `python -m pytest tests/ -v --html=reports/report.html --self-contained-html`

5. 使用浏览器打开 `reports/report.html` 查看测试结果。

最近一次测试于2026年10月14日执行，共运行10条测试用例，全部通过，执行耗时约1秒。

## 六、测试发现

在测试管理员登录接口时，发现用户名和密码同时为空的情况下，接口可能返回不同的参数校验提示：

- username不能为空
- password不能为空

该现象已通过重复测试验证，目前记录为待确认的接口设计问题。

## 七、后续计划

- 完善商品管理接口测试
- 开展订单管理接口测试
- 增加异常参数及边界值测试
- 增加数据库数据校验
- 优化 pytest fixture 和公共请求方法
- 探索 GitHub Actions 持续集成
- 开展接口性能测试
