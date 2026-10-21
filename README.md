# ModelFlux 大模型 API 示例：Python、Node.js 与 cURL

ModelFlux 是提供模型 API 接入的在线服务；本仓库是独立的开源客户端示例和使用文档，不包含或运行 ModelFlux 网关服务，也不包含模型权重。你可以用它从命令行、Python 或 Node.js 发起一次普通文本对话请求。

[ModelFlux 官网](https://modelflux.cn/) · [注册与 API Key](https://modelflux.cn/sign-up) · [价格](https://modelflux.cn/pricing) · [文档索引](docs/INDEX.md) · [English](README.en.md)

## 快速开始

### 1. 获取代码并准备 API Key

从公开仓库选择一个托管站点克隆：

```bash
git clone https://github.com/pangxin12345/modelflux-api-examples.git
cd modelflux-api-examples
```

也可以使用 [Gitee 仓库](https://gitee.com/helen_jar/modelflux-api-examples)。在 ModelFlux 账户中创建自己的 API Key。调用可能产生费用，请先查看当前价格；不要使用或分享他人的密钥。

### 2. 设置环境变量

复制模板并在本机编辑 `.env`，填入自己的密钥：

```bash
cp .env.example .env
chmod 600 .env
# 用编辑器在本机编辑 .env，替换密钥占位符
set -a; . ./.env; set +a
```

示例不会自动读取 `.env`。只加载自己创建并检查过的文件，不要提交 `.env` 或把密钥放进截图、日志和公开问题。变量默认值如下：

```text
MODELFLUX_API_KEY=必填：你的密钥
MODELFLUX_BASE_URL=https://modelflux.cn/v1
MODELFLUX_MODEL=deepseek-flash
```

### 3. 运行一个客户端

在仓库根目录，根据本机环境任选一种：

```bash
bash examples/curl/chat.sh
python3 examples/python/chat.py
node examples/node/chat.mjs
```

分别需要 Bash 与 cURL 7.76+、Python 3.10+（标准库）或 Node.js 20+（内置 `fetch`）。cURL 示例可选用首个参数指定 JSON 输出文件，例如 `bash examples/curl/chat.sh response.json`；Python 和 Node.js 示例将 JSON 响应打印到标准输出。Windows 用户可参见[快速开始说明](docs/quickstart.md)设置 PowerShell 环境变量。

## 这组示例做什么

三个客户端都向 `POST /chat/completions` 发送一次非流式文本请求，默认模型标识为 `deepseek-flash`，`max_tokens` 为 128，演示提示词要求模型回复 `ModelFlux connection OK`。示例没有自动重试。三种客户端已于 2026-10-21 在记录的 macOS 环境各完成一次真实调用；响应共报告 216 tokens。详见[验证记录](docs/validation.md)，这不是 SLA、价格计算或其他环境的保证。

普通文本请求成功不代表流式输出、工具调用、多模态、容灾或长期稳定性已验证。“兼容接口”只说明请求入口风格相似，不代表功能和行为全面一致。响应中的模型名称也不是底层模型身份的独立证明。

## 文档

- [按任务浏览全部文档](docs/INDEX.md)
- [快速开始与环境配置](docs/quickstart.md)
- [常见问题](docs/faq.md)
- [模型选择](docs/model-selection.md)
- [兼容范围](docs/compatibility.md)
- [价格与用量](docs/pricing-and-usage.md)
- [故障排查](docs/troubleshooting.md)
- [实际调用验证记录](docs/validation.md)
- [项目信息与证据来源](docs/references.md) · [软件引用元数据](CITATION.cff)
- [CSDN 接入文章草稿](content/csdn/01-api-quickstart.md)
- [贡献指南](CONTRIBUTING.md) · [安全问题报告](SECURITY.md)

## 范围与许可

仓库公开的是接入文档和示例代码，不提供 ModelFlux 网关服务端、模型权重、OpenAI SDK 封装、RAG 实现或全部模型的验证结论。运行示例会访问在线服务，可能产生费用；价格和账户计量以调用时平台信息为准。仓库内容按 MIT 许可证提供；服务另行计费，模型权重不在本仓库许可范围内。项目不声称与任何模型厂商存在官方关联。
