# Mall 商城接口自动化测试项目

一、项目简介

本项目基于 GitHub 开源商城系统 Mall，使用 Python、requests、pytest 对商城后台管理系统进行接口自动化测试。

项目采用 API 接口封装与测试用例分离的设计方式，通过 BaseApi 统一管理 HTTP 请求，通过 LoginApi、ProductApi、CategoryApi、OrderApi 封装业务接口，并使用 pytest 实现测试执行、参数化测试和 Token 认证管理。

目前已完成管理员登录、商品管理、商品分类和订单管理四个模块，共46条接口自动化测试用例，覆盖正常业务流程、未授权访问、分页查询、关键词搜索、订单状态筛选、订单编号查询以及异常参数等场景。

项目支持通过 .env 配置测试环境、使用 pytest-html 生成测试报告，并通过 Git 和 GitHub 进行版本管理。

测试过程中发现的异常接口行为已记录在 docs/bug_report.md 中，便于后续缺陷分析与跟踪。

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

### 商品分类接口

接口地址：

- `GET /productCategory/list/{parentId}`
- `GET /productCategory/{id}`

| 用例编号 | 测试场景 | 测试结果 |
|---|---|---|
| TC_CATEGORY_001 | 正常查询一级商品分类列表 | PASS |
| TC_CATEGORY_002 | 查询一级商品分类第二页 | PASS |
| TC_CATEGORY_003 | 根据父分类ID查询子分类 | PASS |
| TC_CATEGORY_004 | 未登录访问商品分类列表 | PASS |
| TC_CATEGORY_005 | 查询不存在的父分类ID | PASS |
| TC_CATEGORY_006 | 查询指定商品分类详情 | PASS |
| TC_CATEGORY_007 | 页码为0时查询商品分类 | PASS |
| TC_CATEGORY_008 | 每页数量为0时查询商品分类 | PASS |
| TC_CATEGORY_009 | 使用负数父分类ID查询商品分类 | PASS |
| TC_CATEGORY_010 | 查询不存在的商品分类详情ID | PASS |
| TC_CATEGORY_011 | 使用非整数父分类ID查询商品分类 | PASS |

目前已完成11条商品分类接口测试用例，覆盖正常查询、分页查询、子分类查询、未登录访问、不存在的父分类查询、分类详情查询以及非法分页参数测试。

测试中验证了HTTP状态码、业务状态码、分页信息、分类父子关系、分类层级和部分字段的数据类型。

### 订单管理接口

接口地址：

- `GET /order/list`
- `GET /order/{id}`

| 用例编号 | 测试场景 | 测试结果 |
|---|---|---|
| TC_ORDER_001 | 正常查询订单列表 | PASS |
| TC_ORDER_002 | 查询订单列表第二页 | PASS |
| TC_ORDER_003 | 未登录访问订单列表 | PASS |
| TC_ORDER_004 | 根据真实订单ID查询订单详情 | PASS |
| TC_ORDER_005 | 根据订单状态4筛选订单 | PASS |
| TC_ORDER_006 | 根据订单状态0筛选订单 | PASS |
| TC_ORDER_007 | 根据订单状态1筛选订单 | PASS |
| TC_ORDER_008 | 根据订单状态2筛选订单 | PASS |
| TC_ORDER_009 | 根据订单状态3筛选订单 | PASS |
| TC_ORDER_010 | 根据订单状态4进行参数化筛选 | PASS |
| TC_ORDER_011 | 根据真实订单编号查询订单 | PASS |
| TC_ORDER_012 | 查询不存在的订单编号 | PASS |
| TC_ORDER_013 | 查询不存在的订单ID | PASS |
| TC_ORDER_014 | 查询订单ID为0 | PASS |
| TC_ORDER_015 | 查询负数订单ID | PASS |
| TC_ORDER_016 | 查询非数字订单ID | PASS |

目前已完成16条订单管理接口自动化测试用例，覆盖订单列表查询、分页查询、未登录访问、订单状态筛选、订单编号查询、订单详情查询以及异常订单ID等场景。

测试中使用真实订单数据动态获取订单ID和订单编号，避免在正常查询用例中直接写死测试数据。

使用pytest参数化测试多个订单状态，提高测试代码的复用性。

**说明：** 部分异常订单ID测试用于验证后端当前的实际响应行为，测试通过不代表该行为符合业务要求。另外，部分订单状态筛选测试可能返回空列表，仍需结合测试数据进一步验证筛选逻辑。

### 测试执行情况

目前累计完成46条接口自动化测试用例，包括：

- 管理员登录接口：6条
- 商品列表接口：8条
- 商品编辑信息查询接口：5条
- 商品分类接口：11条
- 订单管理接口：16条

最近一次完整测试结果：46 passed in 2.13s（2026年10月）。

全部46条自动化测试用例通过。

项目支持使用pytest-html生成HTML测试报告，便于查看测试结果和执行时间。

## 四、项目目录

```text
mall-api-test/
├── api/
│   ├── __init__.py
│   ├── base_api.py
│   ├── login_api.py
│   ├── product_api.py
│   ├── category_api.py
│   └── order_api.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── data/
│   ├── order_status.json
│   └── login_cases.json
├── utils/
│   ├── __init__.py
│   └── data_loader.py
├── tests/
│   ├── conftest.py
│   ├── test_login.py
│   ├── test_product.py
│   ├── test_category.py
│   └── test_order.py
├── scripts/
│   ├── check_invalid_id.py
│   ├── check_invalid_category_id.py
│   ├── check_order_list.py
│   ├── check_order_status.py
│   ├── check_order_sn.py
│   └── check_invalid_order_id.py
├── run_tests.py
├── docs/
│   └── bug_report.md
├── reports/                 # 本地生成，不提交Git
│   └── test_report.html
├── .env                     # 本地配置，不提交Git
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 五、测试框架设计

本项目使用 Python、Requests 和 pytest 实现接口自动化测试，并通过以下方式优化测试代码的组织和执行效率。

### 1. API 接口封装

项目采用接口请求与测试断言分离的设计方式：

- `BaseApi`：封装通用 GET、POST 请求，统一管理请求地址和超时时间。
- `LoginApi`：封装管理员登录接口。
- `ProductApi`：封装商品列表查询、商品编辑信息查询接口。
- `CategoryApi`：封装商品分类列表及分类详情查询接口。
- `OrderApi`：封装订单列表查询、订单状态和订单编号筛选以及订单详情查询接口。

测试文件通过调用业务 API 类发送请求，并使用 pytest 进行响应结果验证，减少重复代码，提高测试代码的可维护性。

### 2. 公共 Fixture 管理

使用 `tests/conftest.py` 统一管理管理员登录和 Token 获取功能。

通过 `auth_headers` fixture 获取管理员 Token，并自动生成带有 Authorization 的请求头，供商品、商品分类和订单管理等需要认证的测试复用。

将 fixture 作用域设置为 `scope="session"`，使同一次 pytest 测试会话中需要认证的测试共享一次 Token 获取结果，减少重复登录请求。

### 3. 参数化测试与JSON数据驱动

项目使用 `@pytest.mark.parametrize` 实现参数化测试，提高测试用例的复用性。

在此基础上，引入JSON数据驱动，将测试数据与测试代码分离，方便后续维护和扩展。

目前已实现以下数据驱动场景：

- 订单状态筛选：使用 `data/order_status.json` 管理5组订单状态测试数据。
- 登录异常场景：使用 `data/login_cases.json` 管理4组异常登录测试数据。

通过 `utils/data_loader.py` 中的 `load_json_data()` 函数统一读取JSON文件。

测试执行时，pytest自动读取测试数据，并根据每组数据生成独立的测试用例。

其中登录测试通过 `.env` 文件读取测试账号和密码，避免将真实密码直接写入JSON文件。

目前项目仍为46条自动化测试用例，数据驱动改造没有增加重复测试。

### 4. 统一配置与测试报告

通过 `.env` 文件保存测试环境地址、测试账号和密码，并使用 `config/settings.py` 集中读取环境变量。

通过 `BaseApi` 统一设置 HTTP 请求超时时间，避免在不同接口中重复配置。

使用 pytest-html 生成 HTML 测试报告，记录测试执行结果和运行时间，便于查看测试情况。

目前项目共有46条接口自动化测试用例，覆盖管理员登录、商品管理、商品分类和订单管理四个模块，最近一次完整执行全部通过。

### 5. 辅助诊断脚本

项目中的 `scripts/check_invalid_id.py` 是用于分析商品ID参数类型错误的辅助诊断脚本。

该脚本使用 Python Requests，先通过管理员登录接口获取有效Token，再分别请求非法商品ID、正常商品ID以及 `/error` 路径，对比不同请求的响应结果，辅助定位Spring Security异常处理问题。

运行前需确保Mall后端及相关依赖服务正常启动，并已配置 `.env` 文件。

运行命令：

`python scripts/check_invalid_id.py`

该脚本不属于正式的pytest自动化测试用例，相关问题分析见 `docs/bug_report.md`。

此外，项目还包含以下辅助诊断脚本：

- `check_invalid_category_id.py`：分析商品分类ID类型错误的响应。
- `check_order_list.py`：检查订单列表接口的响应结构和分页数据。
- `check_order_status.py`：验证订单状态筛选功能。
- `check_order_sn.py`：验证订单编号查询功能。
- `check_invalid_order_id.py`：检查不存在、负数及非数字订单ID的响应。

这些脚本主要用于接口调试、响应分析和缺陷复现，不计入正式的pytest测试用例数量。

在项目根目录下，可以使用 `python -m scripts.脚本名称` 的方式运行对应脚本。

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

   `python -m pytest tests/ -v --html=reports/test_report.html --self-contained-html`

5. 使用浏览器打开 `reports/test_report.html` 查看测试结果。

最近一次完整测试于2026年10月执行，共运行46条自动化测试用例，全部通过，耗时2.13秒。

### 使用测试运行脚本

项目提供 `run_tests.py` 脚本，用于统一执行全部接口自动化测试，并自动生成带时间戳的HTML测试报告。

运行命令：

```cmd
python run_tests.py
```

每次执行后，测试报告将自动保存到 `reports/` 目录，例如：

`reports/report_20261019_143025.html`

通过时间戳区分不同批次的测试报告，避免覆盖之前的测试结果。

测试执行完成后，可以在浏览器中打开对应HTML文件查看结果。

## 七、测试发现

在测试管理员登录接口时，发现用户名和密码同时为空的情况下，接口可能返回不同的参数校验提示：

- username不能为空
- password不能为空

该现象已通过重复测试验证，目前记录为待确认的接口设计问题。

### 商品分类接口分页参数校验问题（待确认）

在商品分类列表接口测试中发现，当pageNum=0或pageSize=0时，接口仍返回HTTP 200、业务状态码200和“操作成功”，但分类列表为空。

目前已通过Swagger手动测试和pytest参数化测试验证该现象。

由于尚未确认接口是否要求分页参数必须为正整数，因此暂时记录为潜在缺陷。

详细复现步骤和测试结果见docs/bug_report.md。

### 商品ID参数类型错误时返回不恰当的认证提示（已定位原因，待修复）

在商品编辑信息查询接口测试中发现，当商品ID传入非数字字符串 `abc` 时，接口返回HTTP状态码400，但JSON响应中的业务状态码为401，并提示“暂未登录或token已经过期”。

经过测试确认，使用相同的有效Token查询正常商品ID时，接口能够成功返回商品信息，因此该错误提示与实际情况不符。

通过查看Java后端源码，发现该接口使用 `Long` 类型接收商品ID，而全局异常处理器没有专门处理参数类型转换异常。

随后临时修改Spring Security配置，允许 `ERROR` 类型的请求分发。重新编译并测试后，接口返回正常的HTTP 400 Bad Request错误信息。

该实验表明，Spring Security对错误请求分发的访问控制是造成异常提示的重要因素。目前已完成初步原因定位，尚未进行正式修复。

详细分析及验证过程见：`docs/bug_report.md`。


### 商品分类ID参数类型错误时返回不恰当的认证提示

在商品分类列表接口测试中发现，当parentId传入非整数字符串abc时，接口返回HTTP 400，但JSON响应中的业务状态码为401，并提示“暂未登录或token已经过期”。

测试请求已携带有效的管理员Token，因此该提示与实际的参数类型错误不符。

这一现象与商品编辑信息查询接口中发现的问题相似，可能与后端统一异常处理或Spring Security错误请求分发配置有关。

目前已通过Python Requests和pytest复现，具体原因仍需进一步确认。

详细记录见docs/bug_report.md中的缺陷记录2。

### 订单详情接口异常ID处理问题（待修复）

在订单详情接口测试中发现，当订单ID传入非数字字符串 `abc` 时，接口返回HTTP状态码400，但JSON响应中的业务状态码为401，并提示“暂未登录或token已经过期”。

测试请求已经携带有效的管理员Token，且正常订单ID能够成功查询，因此该提示与实际的参数类型错误不符。

该问题与商品和商品分类接口中发现的异常ID处理问题相似，可能与后端参数类型转换异常处理或Spring Security错误请求分发有关，具体原因仍需进一步确认。

另外，当订单ID为999999999、0或-1时，当前接口均返回HTTP 200、业务状态码200，且data为null。

上述行为是否符合接口设计规范，仍需进一步确认。

详细复现步骤和测试结果已记录在 `docs/bug_report.md` 中。

## 八、后续计划

- 继续完善商品管理和订单管理接口测试
- 增加测试数据驱动，提高测试用例复用性
- 完善测试数据准备和清理机制
- 增加数据库数据校验
- 进一步优化公共请求方法和测试数据管理
- 优化HTML测试报告
- 探索GitHub Actions持续集成
- 开展接口性能测试
