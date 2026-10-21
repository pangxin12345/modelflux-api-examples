# ModelFlux API Examples: Python, Node.js, and cURL

This repository contains small client examples for sending one text chat request to ModelFlux. ModelFlux is the API service; this repository is an independent open-source collection of examples and documentation. It does not include the gateway server or model weights.

[ModelFlux website](https://modelflux.cn/) · [Sign up and create an API key](https://modelflux.cn/sign-up) · [Pricing](https://modelflux.cn/pricing) · [Chinese documentation index](docs/INDEX.md) · [中文 README](README.md)

## Quick start

Clone the GitHub repository, then enter its directory:

```bash
git clone https://github.com/pangxin12345/modelflux-api-examples.git
cd modelflux-api-examples
cp .env.example .env
chmod 600 .env
```

Edit `.env` locally and replace the API key placeholder. The examples do not load `.env` automatically. In macOS or Linux, export its values in the current shell with:

```bash
set -a; . ./.env; set +a
```

Only source a file you created and reviewed. Never commit `.env` or share your key. Calls may incur charges; check the current [pricing](https://modelflux.cn/pricing) first.

Run one example from the repository root:

```bash
bash examples/curl/chat.sh
python3 examples/python/chat.py
node examples/node/chat.mjs
```

Requirements: Bash and cURL 7.76+, Python 3.10+ with the standard library, or Node.js 20+ with built-in `fetch`. The cURL script optionally writes JSON to the first path argument, for example `bash examples/curl/chat.sh response.json`. Python and Node.js print the JSON response to standard output.

## Scope and verification

All three examples send one non-streaming text request to `POST /chat/completions`, with model ID `deepseek-flash`, `max_tokens: 128`, and the same short demonstration prompt. They have no automatic retries. Each client completed one real call on the macOS environment recorded on 2026-10-21; the responses reported 216 tokens in total. See the [validation record](docs/validation.md) for details and limits.

Streaming, tool calls, multimodal input or output, failover, long-term reliability, and model identity have not been verified. “Compatible API” describes a similar request interface, not complete feature or behavior equivalence. A model name returned in a response does not independently establish the underlying model identity. Requests can incur charges; prices and account metering can change.

The repository content is licensed under MIT. The hosted service is billed separately, and model weights are outside this repository and its license. The project does not claim an official relationship with any model provider.

## More information

The complete documentation, FAQ, issue template, and CSDN article draft are currently in Chinese. Start with the [documentation index](docs/INDEX.md), [FAQ](docs/faq.md), [compatibility notes](docs/compatibility.md), [pricing and usage](docs/pricing-and-usage.md), and [troubleshooting guide](docs/troubleshooting.md). See also [contributing](CONTRIBUTING.md) and [security reporting](SECURITY.md).
