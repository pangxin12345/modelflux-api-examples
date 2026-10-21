#!/usr/bin/env bash
# Run from the repository root. Optional argument: output JSON file.
set -euo pipefail

: "${MODELFLUX_API_KEY:?Set MODELFLUX_API_KEY first (see docs/quickstart.md)}"
if [[ "$MODELFLUX_API_KEY" == "replace-with-your-own-key" || "$MODELFLUX_API_KEY" == *[$'\r\n\t '\"\\]* ]]; then
  echo 'Invalid API key: replace the placeholder; whitespace, quotes and backslashes are not allowed.' >&2
  exit 2
fi
base_url="${MODELFLUX_BASE_URL:-https://modelflux.cn/v1}"
model="${MODELFLUX_MODEL:-deepseek-flash}"
if [[ "$base_url" != https://?* || "$base_url" == *[$'\r\n\t ']* || "$base_url" == *[@\?\#]* ]]; then
  echo 'MODELFLUX_BASE_URL must be an HTTPS URL without credentials, query, fragment or whitespace.' >&2
  exit 2
fi
if [[ ! "$model" =~ ^[a-zA-Z0-9._:/-]+$ ]]; then
  echo 'MODELFLUX_MODEL contains unsupported characters.' >&2
  exit 2
fi
if [[ $# -gt 1 ]]; then
  echo 'Usage: bash examples/curl/chat.sh [output.json]' >&2
  exit 2
fi
if [[ $# -eq 1 ]]; then set -- --output "$1"; else set --; fi
# Pass the auth header via stdin instead of placing its value in curl argv.
# No redirect following, no retries, at most 128 output tokens.
curl --silent --show-error --fail-with-body \
  --connect-timeout 15 --max-time 90 \
  --proto '=https' \
  --url "${base_url%/}/chat/completions" \
  --config - \
  --header 'Content-Type: application/json' \
  --data "{\"model\":\"${model}\",\"messages\":[{\"role\":\"user\",\"content\":\"Reply with exactly: ModelFlux connection OK\"}],\"stream\":false,\"max_tokens\":128}" \
  "$@" <<EOF
header = "Authorization: Bearer ${MODELFLUX_API_KEY}"
EOF
