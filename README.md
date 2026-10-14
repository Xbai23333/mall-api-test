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


### 商品列表接口

接口地址：`GET /product/list`

| 用例编号 | 测试场景 | 测试结果 |
|---|---|---|
| TC_PRODUCT_001 | 正常查询商品列表 | PASS |
| TC_PRODUCT_002 | 商品列表分页查询 | PASS |
| TC_PRODUCT_003 | 商品关键词搜索 | PASS |
| TC_PRODUCT_004 | 未登录访问商品列表 | PASS |
| TC_PRODUCT_005 | 页码为0 | PASS |
| TC_PRODUCT_006 | 页码为负数 | PASS |
| TC_PRODUCT_007 | 每页数量为0 | PASS |
| TC_PRODUCT_008 | 每页数量为负数 | PASS |

**说明：** 4条异常分页参数测试用于验证接口当前的实际行为。测试通过不代表非法参数的处理符合业务要求，相关问题已记录，等待进一步确认。

### 商品编辑信息查询接口

接口地址：`GET /product/updateInfo/{id}`

| 用例编号 | 测试场景 | 测试结果 |
|---|---|---|
| TC_PRODUCT_009 | 查询存在的商品ID | PASS |
| TC_PRODUCT_010 | 查询不存在的商品ID | PASS |
| TC_PRODUCT_011 | 商品ID为0 | PASS |
| TC_PRODUCT_012 | 商品ID为负数 | PASS |
| TC_PRODUCT_013 | 商品ID为非数字字符串 | PASS |

目前已完成5条商品编辑信息查询接口测试用例，包括正常商品查询、不存在的商品ID及非法商品ID等场景。

**说明：** 非数字商品ID测试用于记录接口原始配置下的实际响应行为。测试通过不代表该响应符合接口设计要求，相关问题已记录在缺陷报告中。

### 测试执行情况

目前累计完成 **19条接口自动化测试用例**，包括：

- 管理员登录接口：6条
- 商品列表接口：8条
- 商品编辑信息查询接口：5条

最近一次完整测试结果：`19 passed in 1.03s`。

**说明：** 该结果是在后端原始安全配置下取得的。后续临时修改Spring Security配置进行了缺陷定位实验，实验结束后已恢复源代码，但需要重新编译并重启后端，才能恢复原来的运行环境。


## 四、项目目录

```text
mall-api-test/
├── tests/
│   ├── conftest.py
│   ├── test_login.py
│   └── test_product.py
├── docs/
│   └── bug_report.md
├── reports/
│   └── report.html
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 五、测试框架设计

本项目使用 Python、Requests 和 pytest 实现接口自动化测试，并通过以下方式优化测试代码的组织和执行效率。

### 1. 公共 Fixture 管理

使用 `conftest.py` 统一管理管理员登录和 Token 获取功能，其他测试文件可以直接使用 `auth_headers`，避免重复编写登录代码。

将 `auth_headers` 的作用域设置为 `scope="module"`，使同一测试模块中的用例能够复用 Token，减少重复登录请求。

### 2. 参数化测试

使用 `@pytest.mark.parametrize` 实现参数化测试，将多个分页边界值测试场景合并到同一个测试函数中，减少重复代码，同时保留不同测试场景的覆盖。

### 3. 测试环境配置

使用 `.env` 文件管理接口地址、测试账号和密码，并通过 `.gitignore` 排除敏感配置文件，避免将账号密码提交到 GitHub。

### 4. 自动化测试报告

使用 pytest-html 生成 HTML 测试报告，记录测试用例的执行结果和运行时间，方便查看和分析测试结果。

目前项目共有14条自动化测试用例，最近一次执行全部通过。

## 六、运行方法
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

最近一次测试于2026年10月14日执行，共运行14条自动化测试用例，全部通过，执行耗时约0.92秒，并成功生成 HTML 测试报告。

## 七、测试发现

在测试管理员登录接口时，发现用户名和密码同时为空的情况下，接口可能返回不同的参数校验提示：

- username不能为空
- password不能为空

该现象已通过重复测试验证，目前记录为待确认的接口设计问题。

### 商品列表分页参数校验问题（待确认）

在商品列表接口测试中发现，当 `pageNum` 或 `pageSize` 为0、负数时，接口仍然返回业务状态码200和“操作成功”，但商品列表为空。

目前已通过 Swagger 和 pytest 自动化测试复现该现象。

由于尚未确认接口对分页参数的正式校验要求，暂时记录为潜在缺陷。


### 商品ID参数类型错误时返回不恰当的认证提示（已定位原因，待修复）

在商品编辑信息查询接口测试中发现，当商品ID传入非数字字符串 `abc` 时，接口返回HTTP状态码400，但JSON响应中的业务状态码为401，并提示“暂未登录或token已经过期”。

经过测试确认，使用相同的有效Token查询正常商品ID时，接口能够成功返回商品信息，因此该错误提示与实际情况不符。

通过查看Java后端源码，发现该接口使用 `Long` 类型接收商品ID，而全局异常处理器没有专门处理参数类型转换异常。

随后临时修改Spring Security配置，允许 `ERROR` 类型的请求分发。重新编译并测试后，接口返回正常的HTTP 400 Bad Request错误信息。

该实验表明，Spring Security对错误请求分发的访问控制是造成异常提示的重要因素。目前已完成初步原因定位，尚未进行正式修复。

详细分析及验证过程见：`docs/bug_report.md`。

## 八、后续计划

- 完善商品管理接口测试
- 开展订单管理接口测试
- 增加异常参数及边界值测试
- 增加数据库数据校验
- 进一步优化公共请求方法和测试数据管理
- 探索 GitHub Actions 持续集成
- 开展接口性能测试
