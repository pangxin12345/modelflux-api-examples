# 快速开始

本文说明如何配置环境并运行仓库中的三种最小示例。资料整理日期：2026-10-21。

## 准备

先在 [ModelFlux 官网](https://modelflux.cn/sign-up)注册并获取 API Key。调用服务可能收费，运行前请查看[当前价格](https://modelflux.cn/pricing)。不要把真实密钥提交到 Git、粘贴到问题或写入示例文件。

按所选示例安装运行环境：

- Bash 与 cURL 7.76+（使用 `--fail-with-body`）
- Python 3.10 或更高版本；仅使用标准库
- Node.js 20 或更高版本；使用内置 `fetch`

## 配置环境变量

示例读取以下变量：

| 变量 | 必需 | 默认值 | 用途 |
|---|---|---|---|
| `MODELFLUX_API_KEY` | 是 | 无 | API 密钥 |
| `MODELFLUX_BASE_URL` | 否 | `https://modelflux.cn/v1` | API 基础地址 |
| `MODELFLUX_MODEL` | 否 | `deepseek-flash` | 请求使用的模型标识 |

根目录 `.env.example` 是手动配置模板，脚本不会自动加载 `.env`。macOS/Linux 可按以下步骤操作：

```bash
cp .env.example .env
# 手动编辑 .env，替换占位符
set -a; . ./.env; set +a
```

Windows PowerShell 可在当前终端设置变量，再运行 Python 或 Node 示例：

```powershell
$env:MODELFLUX_API_KEY = "你的密钥"
$env:MODELFLUX_BASE_URL = "https://modelflux.cn/v1"
$env:MODELFLUX_MODEL = "deepseek-flash"
```

示例不提供密钥，也不应将上述占位文本原样当作密钥使用。

## 运行

从仓库根目录执行：

```bash
bash examples/curl/chat.sh
python3 examples/python/chat.py
node examples/node/chat.mjs
```

三者都会向 `POST /chat/completions` 发送一次非流式文本对话请求，默认模型为 `deepseek-flash`，最大生成长度为 128 tokens。curl 示例可接收可选的首个参数作为 JSON 文件输出路径，例如 `bash examples/curl/chat.sh response.json`；Python 和 Node 示例将 JSON 响应写到标准输出。

示例没有自动重试。若请求失败，请先检查 HTTP 状态码、响应中的错误正文、环境变量和账户用量；参见[故障排查](troubleshooting.md)。成功返回也可能产生费用。

正常响应应包含非空的 `choices[0].message.content`。本仓库的演示提示词要求返回 `ModelFlux connection OK`；模型回答不保证每次逐字相同。实际验证的响应字段摘录见 [response-excerpt.json](response-excerpt.json)。

本机 `.env` 不应分享。macOS/Linux 建议复制模板后运行 `chmod 600 .env`。加载 `.env` 使用的是 shell 语法，只加载自己创建并检查过的文件。不要把密钥粘贴到公开命令记录或截图中。测试结束可运行 `unset MODELFLUX_API_KEY`。
