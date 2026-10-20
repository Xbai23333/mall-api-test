# Mall 商城接口自动化测试项目

![Unit Tests](https://github.com/Xbai23333/mall-api-test/actions/workflows/ci.yml/badge.svg)
[![Mall Full API Tests](https://github.com/Xbai23333/mall-api-test/actions/workflows/full-api-tests.yml/badge.svg)](https://github.com/Xbai23333/mall-api-test/actions/workflows/full-api-tests.yml)

**在线测试报告：** [点击查看 Allure 可视化测试报告](https://xbai23333.github.io/mall-api-test/)

**测试项目文档：** [50条自动化测试用例清单](docs/测试用例清单.md) | [接口缺陷报告](docs/bug_report.md)

项目已实现 GitHub Actions 持续集成，支持自动启动测试环境、执行50条自动化测试、生成 Allure 报告，并通过 GitHub Pages 自动发布。

## 一、项目简介

本项目基于 GitHub 开源商城系统 Mall，使用 Python、requests 和 pytest 搭建接口自动化测试框架，对商城后台管理系统进行自动化测试。

项目采用分层设计，将接口请求封装、测试用例、测试数据、公共断言和环境配置进行分离，提高测试代码的复用性和可维护性。

目前共完成50条自动化测试用例，其中包括46条接口测试和4条公共断言工具函数单元测试。

接口测试覆盖管理员登录、商品管理、商品分类和订单管理四个模块，包含正常业务流程、Token 认证、分页查询、关键词搜索、订单状态筛选、订单编号查询以及异常参数等场景。

项目支持 JSON 数据驱动、pytest Fixture、统一日志管理、环境变量配置，以及 pytest-html 和 Allure 可视化测试报告。

其中，Allure 报告支持中文测试标题、功能模块分类和参数化测试结果展示。项目已通过 GitHub Actions 实现自动执行测试、生成报告和上传测试结果。

此外，项目已接入 GitHub Actions 持续集成，实现自动启动 MySQL、Redis、Mall Java 后端、初始化测试数据库及管理员账号，并执行完整自动化测试。

目前完整测试工作流支持在代码推送到 main 分支后自动触发，也可以手动运行。

2026年10月，GitHub Actions 云端完整测试结果为：50 passed，0 failed，测试通过率100%。

测试过程中发现的潜在接口缺陷已记录在 docs/bug_report.md 中，方便后续分析与跟踪。

## 二、技术栈

- 后端系统：Java 17、Spring Boot、MySQL 5.7、Redis 7
- 接口测试：Python 3.11、requests、Swagger
- 测试框架：pytest
- 数据驱动：JSON、pytest.mark.parametrize
- 测试管理：pytest Fixture、公共断言、日志记录
- 测试报告：pytest-html、Allure 2.46.1
- 持续集成：GitHub Actions
- 后端构建：Maven
- CI 环境：Ubuntu 24.04、MySQL 和 Redis 服务容器
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

目前项目共完成50条自动化测试用例。

| 测试模块 | 用例数量 |
|---|---:|
| 管理员登录接口 | 6 |
| 商品列表接口 | 8 |
| 商品编辑信息查询接口 | 5 |
| 商品分类接口 | 11 |
| 订单管理接口 | 16 |
| 公共断言工具函数单元测试 | 4 |
| **合计** | **50** |

其中，46条为需要 Mall 后端环境的接口自动化测试，另外4条为不依赖后端服务的公共断言工具函数单元测试。

2026年10月，GitHub Actions 完整测试结果：

- 测试总数：50
- 通过数量：50
- 失败数量：0
- 测试通过率：100%
- pytest 执行耗时：2.42秒

项目支持通过 pytest-html 和 Allure 自动生成测试报告。其中，pytest-html 用于展示测试执行结果，Allure 提供中文测试标题、模块分类、执行时间及测试详情等可视化功能。

GitHub Actions 会在完整测试执行后自动生成测试报告，并上传 pytest-html 报告、Allure 原始结果和 Allure HTML 报告，方便下载和查看。

需要说明的是，测试通过代表实际响应符合当前测试用例中的预期断言，并不意味着所有接口行为都符合业务设计规范。已发现的潜在缺陷仍记录在 docs/bug_report.md 中。

## 四、项目目录

```text
mall-api-test/
├── .github/
│   └── workflows/
│       ├── ci.yml                  # 4条单元测试
│       └── full-api-tests.yml      # 50条完整自动化测试
├── api/
│   ├── base_api.py                 # HTTP请求统一封装
│   ├── login_api.py                # 登录接口
│   ├── product_api.py              # 商品接口
│   ├── category_api.py             # 商品分类接口
│   └── order_api.py                # 订单接口
├── config/
│   └── settings.py                 # 环境变量配置
├── data/
│   ├── login_cases.json            # 登录测试数据
│   └── order_status.json           # 订单状态测试数据
├── tests/
│   ├── conftest.py                 # pytest Fixture
│   ├── test_assertions.py          # 4条公共断言单元测试
│   ├── test_login.py
│   ├── test_product.py
│   ├── test_category.py
│   └── test_order.py
├── utils/
│   ├── assertions.py               # 公共断言
│   ├── data_loader.py              # JSON数据读取
│   └── logger.py                   # 日志管理
├── scripts/
│   ├── init_ci_admin.sql           # CI管理员角色初始化
│   └── check_*.py                  # 接口辅助诊断脚本
├── docs/
│   ├── bug_report.md               # 缺陷记录
│   └── 测试用例清单.md              # 50条测试用例
├── reports/                         # 测试报告，不提交Git
├── logs/                            # 运行日志，不提交Git
├── .env                             # 本地环境配置，不提交Git
├── .env.example                     # 环境变量示例
├── .gitignore
├── requirements.txt
├── run_tests.py
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

数据驱动改造没有增加重复测试用例。目前项目共有46条接口自动化测试用例，另有4条公共断言工具函数单元测试，合计50条自动化测试。

### 4. 统一配置与测试报告

通过 `.env` 文件保存测试环境地址、测试账号和密码，并使用 `config/settings.py` 集中读取环境变量。

通过 `BaseApi` 统一设置 HTTP 请求超时时间，避免在不同接口中重复配置。

使用 pytest-html 生成 HTML 测试报告，记录测试执行结果和运行时间，便于查看测试情况。

目前项目共有46条接口自动化测试用例，覆盖管理员登录、商品管理、商品分类和订单管理四个模块。此外，还有4条公共断言工具函数单元测试。GitHub Actions 最近一次完整执行共50条测试，全部通过。

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

### 6. GitHub Actions 持续集成

项目已接入 GitHub Actions，实现自动化测试的持续集成。

目前配置了两个独立的工作流：

**（1）单元测试工作流：ci.yml**

主要执行公共断言工具函数的4条单元测试。

该工作流不依赖 Mall 后端、MySQL 或 Redis，因此运行速度较快，适合进行基础代码检查。

**（2）完整接口测试工作流：full-api-tests.yml**

负责搭建完整测试环境，并执行全部50条自动化测试。

执行流程如下：

1. 检出 Python 自动化测试项目和 Mall Java 后端源码。
2. 配置 Java 17、Maven 和 Python 3.11 环境。
3. 启动 MySQL 5.7、Redis 7 服务容器。
4. 导入 Mall 数据库初始化脚本。
5. 编译并启动 Mall Java 后端。
6. 等待后端 HTTP 服务就绪。
7. 注册 CI 专用管理员并分配超级管理员角色。
8. 使用 pytest 执行全部50条自动化测试。
9. 生成 pytest-html 测试报告和 Allure 原始测试结果。
10. 自动生成 Allure HTML 可视化报告。
11. 将三类测试报告上传为 GitHub Actions Artifact。

完整测试工作流支持两种触发方式：

- 向 main 分支推送代码时自动运行。
- 在 GitHub Actions 页面手动点击 Run workflow 运行。

CI 中通过 GitHub Secrets 管理数据库密码和测试管理员密码，避免将真实凭据直接提交到代码仓库。

项目使用独立的临时测试数据库，不会修改本地 MySQL 数据。

2026年10月，完整接口测试工作流已成功运行，测试结果为50 passed、0 failed。

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

最近一次 GitHub Actions 完整测试于2026年10月执行，共运行50条自动化测试用例，全部通过，pytest 执行耗时2.42秒。

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

### Allure 可视化测试报告

项目已集成 Allure 测试报告，用于展示自动化测试的执行结果，并通过 GitHub Actions 自动生成完整的 HTML 报告。

**在线报告地址：**

https://xbai23333.github.io/mall-api-test/

项目已通过 GitHub Pages 实现 Allure 报告自动发布。每次向 `main` 分支推送代码后，GitHub Actions 会执行完整接口测试，并在测试和报告生成成功后自动更新在线报告。

无需下载 ZIP 文件或启动本地服务器，即可通过浏览器查看测试结果。

**主要功能：**

- 使用中文标题展示测试用例，方便阅读。
- 通过 Epic、Feature、Story 对测试用例进行分类。
- 展示测试通过率、执行时间及测试详情。
- 支持参数化测试用例的独立展示。
- GitHub Actions 自动生成并上传 Allure HTML 报告。

**本地生成 Allure 报告：**

首先安装 Python 依赖，并确保已经安装 Allure Commandline。

执行测试并生成 Allure 原始结果：

```bash
python -m pytest tests/ -q --alluredir=reports/allure-results --clean-alluredir
```

生成 HTML 报告：

```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

打开报告：

```bash
allure open reports/allure-report
```

如果 Allure Commandline 没有配置到系统 PATH，可以使用本地安装目录中的 `allure.bat` 执行上述命令。

**GitHub Actions 自动生成报告：**

每次向 `main` 分支推送代码后，GitHub Actions 会自动执行完整测试，并上传以下三个 Artifact：

| Artifact 名称 | 说明 |
|---|---|
| `mall-full-api-test-report` | pytest-html 测试报告 |
| `mall-allure-results` | Allure 原始测试结果 |
| `mall-allure-html-report` | Allure HTML 可视化报告 |

**查看云端 Allure 报告：**

1. 打开 GitHub 仓库的 Actions 页面。
2. 进入最新一次成功的 `Mall Full API Tests` 工作流。
3. 在 Artifacts 区域下载 `mall-allure-html-report`。
4. 解压 ZIP 文件。
5. 在解压后的报告目录中启动本地 HTTP 服务：

```bash
python -m http.server 8765
```

6. 在浏览器中访问 `http://127.0.0.1:8765` 查看报告。

目前 GitHub Actions 已成功执行全部50条自动化测试，并自动生成 Allure HTML 报告。下载后的报告已验证能够正常展示50条测试结果及中文测试标题。

### GitHub Actions 云端运行

项目已经配置 GitHub Actions，可以在云端自动搭建测试环境并执行全部自动化测试。

工作流文件：

- `.github/workflows/ci.yml`
- `.github/workflows/full-api-tests.yml`

手动运行步骤：

1. 打开项目 GitHub 仓库。
2. 点击 Actions。
3. 选择 Mall Full API Tests。
4. 点击 Run workflow，选择 main 分支。
5. 等待工作流执行完成。

完整测试工作流也会在向 main 分支推送代码后自动运行。

运行完成后，可以在对应的 GitHub Actions 运行记录中查看 pytest 测试结果。

工作流运行完成后，可以在 GitHub Actions 运行记录的 Artifacts 区域下载测试报告，包括 `mall-full-api-test-report`、`mall-allure-results` 和 `mall-allure-html-report`。

其中，`mall-allure-html-report` 为自动生成的 Allure 可视化报告，具体查看方法见上方“Allure 可视化测试报告”小节。

项目仓库地址：

https://github.com/Xbai23333/mall-api-test

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

- 继续增加商品管理、订单管理等接口测试场景。
- 完善测试数据准备与清理机制，提高测试独立性。
- 增加数据库数据校验，验证接口操作与数据库状态的一致性。
- 优化测试用例设计，减少对固定测试数据的依赖。
- 进一步完善异常参数和接口权限测试。
- 优化 HTML 测试报告和失败日志分析。
- 学习接口性能测试，探索 JMeter 等测试工具。
