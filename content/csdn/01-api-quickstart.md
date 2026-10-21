# 大模型 API 接入入门：用 cURL 跑通对话请求，以 ModelFlux 为例

开发 AI 应用时，可以先用一个最小请求检查三件事：地址是否正确、密钥是否有效、目标模型是否可用。把这一步验证清楚，再接入业务代码，遇到问题时更容易定位原因。

本文由 ModelFlux 项目维护方整理，以一次普通文本对话介绍接入方法。示例已于 2026 年 10 月 21 日在 macOS 上完成真实调用验证；本文只讨论非流式文本对话。

配套代码：[GitHub 示例仓库](https://github.com/pangxin12345/modelflux-api-examples)；中国镜像：[Gitee 示例仓库](https://gitee.com/helen_jar/modelflux-api-examples)。仓库提供完整脚本、配置模板与实测记录。

## 一、先认识三个配置

| 配置 | 作用 | 本文示例 |
|---|---|---|
| Base URL | API 的基础地址 | `https://modelflux.cn/v1` |
| API Key | 请求鉴权 | 使用你自己的密钥，通过环境变量传入 |
| model | 请求使用的模型标识 | `deepseek-flash` |

ModelFlux 在普通对话场景使用的完整请求地址为：

```text
https://modelflux.cn/v1/chat/completions
```

配置现有客户端时，先看它要求填写“基础地址”还是“完整端点”。如果客户端会自动拼接 `/chat/completions`，再填完整端点就可能造成路径重复。

运行前，请在自己的账户中创建密钥，确认模型权限、账户状态与当前价格。免费注册不等于免费调用；本文不提供共享密钥。

## 二、配置运行环境

本文使用 Bash 和 cURL 7.76 或更高版本。示例项目同时提供 Python 标准库和 Node.js 内置 fetch 两种写法，不需要安装第三方 SDK。

进入示例项目根目录后，复制配置模板：

```bash
cp .env.example .env
chmod 600 .env
```

用编辑器打开 `.env`，替换 `MODELFLUX_API_KEY` 的占位值。其他两项保持如下配置即可：

```text
MODELFLUX_BASE_URL=https://modelflux.cn/v1
MODELFLUX_MODEL=deepseek-flash
```

然后在当前 Bash 终端加载自己编辑的文件：

```bash
set -a
. ./.env
set +a
```

脚本不会自动读取 `.env`。上面的命令使用 shell 语法，因此只应加载自己创建并检查过的文件；密钥也不要提交到仓库或放进截图。

## 三、发送一次最小对话请求

运行仓库中的 cURL 示例：

```bash
bash examples/curl/chat.sh response.json
```

脚本向 `/chat/completions` 发起一次 POST，请求体如下：

```json
{
  "model": "deepseek-flash",
  "messages": [
    {
      "role": "user",
      "content": "Reply with exactly: ModelFlux connection OK"
    }
  ],
  "stream": false,
  "max_tokens": 128
}
```

鉴权使用 `Authorization: Bearer` 请求头。脚本通过标准输入将该请求头交给 cURL，避免把密钥值放入 cURL 的命令行参数。没有开启自动重试，也不会跟随重定向。

使用 Python 打开响应文件，查看实际结果：

```bash
python3 -m json.tool response.json
```

下面是本次 cURL 实测响应的部分字段，已省略请求标识及其他字段：

```json
{
  "model": "deepseek-v4.1-flash",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "ModelFlux connection OK"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 39,
    "completion_tokens": 35,
    "total_tokens": 74
  }
}
```

判断是否跑通，重点看命令是否成功退出，以及 `choices[0].message.content` 是否包含有效文本。不要仅凭网页可打开或接口有响应，就认为调用已经成功。

本次请求填入的是 `deepseek-flash`，响应的 `model` 字段返回 `deepseek-v4.1-flash`。这里如实记录接口行为；返回字符串本身不能证明底层模型身份或渠道来源。

## 四、Python 和 Node.js 怎么调用

如果项目使用 Python 3.10+，可以直接运行标准库版本：

```bash
python3 examples/python/chat.py
```

如果使用 Node.js 20+，可以运行内置 fetch 版本：

```bash
node examples/node/chat.mjs
```

两种写法使用相同的环境变量和请求体，均在标准输出打印 JSON 响应。HTTP 错误只输出状态码或概括信息，详细排查可结合自己的私有控制台调用记录。

本次三个客户端的验证结果如下：

| 客户端 | 结果 | 总耗时 | 服务端返回总 tokens |
|---|---|---:|---:|
| cURL 8.7.1 | 成功，返回指定文本 | 3.073 秒 | 74 |
| Python 3.13.5 | 成功，返回指定文本 | 2.980 秒 | 74 |
| Node.js 26.8.2 | 成功，返回指定文本 | 2.489 秒 | 68 |

耗时包括本机进程启动与网络时间，不是首 token 延迟；每种写法只执行了一次，不能用这组数据比较客户端性能或推断长期稳定性。运行环境下限表示代码要求，不表示这些版本和各操作系统都已逐一验证。

## 五、调用失败时，优先检查这些地方

| 现象 | 优先检查 |
|---|---|
| 400 | JSON 是否正确、参数是否被目标模型支持 |
| 401 / 403 | 密钥是否有效，账户及密钥是否有模型权限 |
| 404 | 基础地址、完整路径和模型标识是否正确 |
| 429 | 请求频率、并发限制、额度及错误正文 |
| 超时 / 5xx | 网络和服务状态，结合私有调用日志判断 |

状态码只是线索，应结合响应正文中的具体错误判断。cURL 示例会保留 HTTP 错误正文；Python 和 Node.js 示例不会直接打印可能包含私有细节的错误正文。

不要把失败请求放进无限重试循环。尤其是客户端超时时，服务端可能已经处理了请求，重复发送前应先检查记录。

## 六、接入业务前，再补一轮验证

最小请求跑通后，建议使用少量真实业务样例检查输出质量、输入长度、响应耗时和用量。示例里的 `max_tokens: 128` 只是短输出演示配置，不能直接代表业务所需的生成长度。

如果要换模型，先确认目标模型使用相同接口，并验证业务依赖的参数和能力。普通文本对话成功，不能推断流式输出、工具调用、图片输入或自动容灾也已通过。

最后到自己的调用记录里核对模型、用量与实际扣费。本次三次请求的响应共报告 216 tokens，但本文没有据此推算价格，也没有核实账单金额。模型列表和价格会变化，请以调用时的账户规则为准。

测试结束后，可以从当前终端移除密钥变量：

```bash
unset MODELFLUX_API_KEY
```

示例仓库开放接入文档和客户端示例，采用 MIT 许可证；不包含网关服务端或模型权重。完整源码、配置模板及验证范围随示例项目一并提供。
