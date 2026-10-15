# Bug-001：商品列表接口未明确拒绝非法分页参数

## 一、基本信息

- 问题编号：BUG-001
- 测试模块：商品管理
- 接口地址：`GET /product/list`
- 问题类型：参数校验问题（待确认）
- 严重程度：暂定低
- 当前状态：待确认需求

## 二、问题描述

在测试商品列表接口时，发现当分页参数 `pageNum` 或 `pageSize` 为0、负数时，接口仍然返回 HTTP 200、业务状态码200和“操作成功”，但商品列表为空。

目前尚未确认接口是否要求分页参数必须为正整数，因此将该现象记录为潜在缺陷。

## 三、复现步骤

1. 启动 Mall 商城后台服务。
2. 打开 Swagger 接口文档。
3. 使用管理员账号登录并完成 Token 授权。
4. 找到 `GET /product/list` 接口。
5. 将商品筛选条件设置为 `{}`。
6. 分别输入以下分页参数并执行请求。

| 测试场景 | pageNum | pageSize |
|---|---:|---:|
| 页码为0 | 0 | 5 |
| 页码为负数 | -1 | 5 |
| 每页数量为0 | 1 | 0 |
| 每页数量为负数 | 1 | -1 |

## 四、实际结果

四组异常参数均返回 HTTP 200、业务状态码200和“操作成功”。

当 `pageNum` 为0或-1时，商品列表为空，总页数为4。

当 `pageSize` 为0或-1时，商品列表为空，总页数为0。

测试环境中商品总数为20条。

## 五、预期结果（待需求确认）

如果接口要求 `pageNum` 和 `pageSize` 必须为正整数，那么对于0或负数，应返回明确的参数错误提示，而不是直接返回“操作成功”。

如果系统设计允许此类参数，则需要在接口文档中明确对应的处理规则。

## 六、问题影响

非法分页参数返回成功状态，可能使调用方难以区分参数错误和正常查询结果为空的情况。

## 七、测试结论

目前已通过 Swagger 手动测试及 pytest 自动化测试复现上述现象。

需要进一步核对接口文档或与开发人员确认参数校验规则，再判断是否属于正式缺陷。


## 缺陷记录2：商品ID参数类型错误时返回不恰当的认证提示

### 1. 问题描述

在 Java Mall 管理后台的商品编辑信息查询接口中，当商品ID传入非数字字符串时，接口返回HTTP 400，但JSON响应内容却提示用户未登录或Token已过期。

实际测试中使用了有效的管理员Token，因此该提示与真实错误原因不符，容易误导接口调用者。

### 2. 测试环境

- 测试项目：Java Mall
- 测试接口：GET /product/updateInfo/{id}
- 测试工具：Python Requests、pytest
- 后端框架：Spring Boot、Spring Security
- 测试日期：2026-10-14

### 3. 复现步骤

1. 启动Java Mall管理后台。
2. 调用POST /admin/login，获取有效的管理员Token。
3. 在请求头中携带Authorization: Bearer Token。
4. 请求GET /product/updateInfo/abc。
5. 查看HTTP状态码及响应内容。

### 4. 实际结果

HTTP状态码：400

响应内容：

{
  "code": 401,
  "message": "暂未登录或token已经过期",
  "data": "Full authentication is required to access this resource"
}

使用相同Token请求GET /product/updateInfo/1，可以正常返回商品信息。

### 5. 预期结果

接口应返回明确的参数类型错误提示，例如HTTP 400 Bad Request，而不是错误地提示用户未登录。

### 6. 原因分析

通过查看Java后端源码，发现：

1. PmsProductController中的商品查询接口使用@PathVariable Long id接收商品ID。
2. 字符串abc无法转换为Long类型。
3. GlobalExceptionHandler没有专门处理MethodArgumentTypeMismatchException。
4. Spring Security配置中没有明确放行ERROR类型的请求分发。
5. 认证失败处理器RestAuthenticationEntryPoint会生成401业务响应。

综合判断，参数类型转换失败后的错误处理流程受到Spring Security访问控制影响，是导致错误认证提示的关键因素。

### 7. 验证过程

在本地开发环境中，临时添加以下配置：

registry.dispatcherTypeMatchers(DispatcherType.ERROR).permitAll();

重新编译并启动后端，再次请求：

GET /product/updateInfo/abc

结果变为：

HTTP状态码：400

{
  "timestamp": "2026-10-14T14:32:20.381+00:00",
  "status": 400,
  "error": "Bad Request",
  "path": "/product/updateInfo/abc"
}

正常商品查询仍然成功。

这一对照实验支持了Spring Security错误分发权限配置影响异常响应的判断。

实验结束后，已从源代码中删除临时配置。

### 8. 处理建议

建议开发人员检查Spring Security对ERROR类型请求分发的访问控制，并完善参数类型转换异常的统一处理，确保接口返回准确、清晰的错误信息。

### 9. 缺陷状态

已复现并完成初步原因定位，尚未实施正式修复。

### 10. 其他接口的相似问题

在商品分类列表接口中发现了相似现象。

测试接口：

GET /productCategory/list/abc?pageNum=1&pageSize=5

测试前已通过管理员登录接口成功获取Token，并在请求头中携带有效的Authorization信息。

实际返回：

HTTP状态码：400

```json
{
  "code": 401,
  "message": "暂未登录或token已经过期",
  "data": "Full authentication is required to access this resource"
}
```

由于parentId参数预期为整数，而实际传入字符串abc，因此该请求属于参数类型错误。

但接口返回的JSON内容却提示认证失败，与实际错误原因不符。

这一现象与商品编辑信息查询接口的异常响应相似，提示两者可能受到相同的全局异常处理或Spring Security配置影响。

目前尚未对商品分类接口单独进行源码定位，因此具体原因仍需进一步确认。

---

## 缺陷记录3：商品分类列表接口未明确拒绝非法分页参数

### 1. 问题描述

在Java Mall管理后台的商品分类列表接口测试中发现，当分页参数pageNum或pageSize为0时，接口仍然返回HTTP 200、业务状态码200和“操作成功”，但商品分类列表为空。

由于目前尚未确认接口是否要求分页参数必须为正整数，因此暂时将该现象记录为潜在缺陷。

### 2. 测试环境

- 测试项目：Java Mall
- 测试接口：GET /productCategory/list/{parentId}
- 测试工具：Swagger、Python Requests、pytest
- 测试日期：2026-10-15
- 问题类型：分页参数校验问题（待确认）
- 严重程度：暂定低

### 3. 复现步骤

1. 启动Java Mall管理后台及相关依赖服务。
2. 使用管理员账号登录，获取有效Token。
3. 打开Swagger，找到GET /productCategory/list/{parentId}接口。
4. 分别输入以下参数并执行请求。

| 测试场景 | parentId | pageNum | pageSize |
|---|---:|---:|---:|
| 页码为0 | 0 | 0 | 5 |
| 每页数量为0 | 0 | 1 | 0 |

### 4. 实际结果

两组异常分页参数均返回HTTP状态码200、业务状态码200和“操作成功”。

具体结果如下：

| 测试场景 | HTTP状态码 | 业务状态码 | total | totalPage | list |
|---|---:|---:|---:|---:|---|
| pageNum=0 | 200 | 200 | 6 | 2 | [] |
| pageSize=0 | 200 | 200 | 6 | 0 | [] |

测试环境中一级商品分类总数为6条。

### 5. 预期结果（待需求确认）

如果接口要求pageNum和pageSize必须为正整数，那么对于0等非法参数，应返回明确的参数错误提示，而不是直接返回“操作成功”。

如果系统设计允许这些参数，则需要在接口文档中明确对应的处理规则。

### 6. 问题分析

当前接口能够返回正确的商品分类总数，但对于不合理的分页参数仍然返回成功状态，可能导致接口调用者无法准确区分参数错误和正常查询结果为空的情况。

该现象与此前商品列表接口的异常分页处理方式类似，可能存在分页参数校验不完善的问题。

目前尚未进一步查看该接口的后端参数校验实现，因此暂时不确定具体原因。

### 7. 验证过程

首先通过Swagger分别发送两组异常分页请求，确认接口返回结果。

随后使用pytest的参数化测试功能，编写以下两条自动化测试用例：

- TC_CATEGORY_007：pageNum=0，pageSize=5
- TC_CATEGORY_008：pageNum=1，pageSize=0

两条测试用例均执行成功。

最近一次完整回归测试结果为：

27 passed in 30.76s

需要说明的是，自动化测试通过仅表示接口当前响应符合测试中记录的实际行为，不代表非法分页参数的处理方式符合业务要求。

### 8. 处理建议

建议进一步确认商品分类接口的分页参数校验规则。

如果要求分页参数必须为正整数，可以在后端增加参数合法性校验，并在参数错误时返回明确的提示信息。

同时建议统一商品列表接口和商品分类列表接口的分页参数处理规则。

### 9. 缺陷状态

待确认需求，尚未进行正式修复。

目前已完成Swagger手动复现和pytest自动化验证，后续需要根据接口设计要求判断是否属于正式Bug。
