# 实际调用验证记录

- 日期：2026-10-21（北京时间），测试开始时间 12:26:59。
- 请求端点：`https://modelflux.cn/v1/chat/completions`。
- 请求模型标识：`deepseek-flash`；响应模型字段：`deepseek-v4.1-flash`。
- 请求参数：`stream: false`、`max_tokens: 128`。
- 演示提示词：`Reply with exactly: ModelFlux connection OK`。
- 环境：macOS，Bash 5.3.15，cURL 8.7.1，Python 3.13.5，Node.js 26.8.2。
- 判定：进程退出码为 0、响应是有效 JSON、`choices[0].message.content` 为非空文本，且不存在顶层 `error`。

| 示例 | 结果 | 客户端总耗时 | 输入 tokens | 输出 tokens | 合计 tokens |
|---|---|---:|---:|---:|---:|
| Bash/cURL | 通过 | 3.073 秒 | 39 | 35 | 74 |
| Python 标准库 | 通过 | 2.980 秒 | 39 | 35 | 74 |
| Node.js fetch | 通过 | 2.489 秒 | 39 | 29 | 68 |
| 合计 | 3/3 通过 | — | 117 | 99 | 216 |

三个响应的可见内容均为 `ModelFlux connection OK`，`finish_reason` 均为 `stop`。耗时为本机测量的完整子进程墙钟时间，包含客户端启动及网络时间，不是首 token 延迟或服务 SLA。用量字段来自服务端响应，没有据此计算或核实实际扣费。

响应字段摘录见 [response-excerpt.json](response-excerpt.json)。原始授权头、密钥、完整请求标识和账户数据没有纳入仓库。

## 范围与限制

每种脚本只做了一次真实正向调用，无自动重试。验证结果仅覆盖当前环境、测试账户及该模型标识的非流式文本对话，不覆盖 Windows/Linux、其他运行时版本、其他模型、流式、工具调用、多模态、并发、容灾、长期稳定性或模型身份真实性。

`deepseek-flash` 与响应字段不同的事实已记录；返回名称不是独立验真证据。运行示例可能计费；价格与账户实际扣费以平台当时规则为准。

离线配置拒绝、语法和文档链接检查由 `python3 scripts/check.py` 执行，不调用收费 API。真实调用后收紧了 cURL 自定义 URL 校验并调整可选输出参数传递，默认请求体与端点不变；使用本地假 cURL 验证正常参数、可选文件输出和授权头传递，没有再次收费调用。检查通过后才可讨论公开发布；Gitee 和 CSDN 发布仍由维护者审阅决定。
