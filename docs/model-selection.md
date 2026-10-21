# 模型选择

示例默认使用 `deepseek-flash`。如需选择其他模型，可在运行脚本前设置 `MODELFLUX_MODEL`：

```bash
export MODELFLUX_MODEL="deepseek-flash"
python3 examples/python/chat.py
```

请求体会将该环境变量的值作为 `model` 字段发送。可用模型名称、能力、上下文限制和计费以 [ModelFlux 模型与价格页面](https://modelflux.cn/pricing)及账户实际可用范围为准；这些信息可能变化。不要仅依据名称推断模型能力，也不要假设不同模型的输出、参数支持或行为完全相同。

本仓库只演示一次普通文本对话，没有对模型质量、延迟、稳定性、工具使用能力或身份真实性进行测评。选择模型前请结合实际任务与价格信息，并先用适当的小请求确认账户可用性。
