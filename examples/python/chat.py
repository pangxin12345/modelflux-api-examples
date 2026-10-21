#!/usr/bin/env python3
"""One non-streaming request using Python 3.10+ standard library only."""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main():
    key = os.environ.get("MODELFLUX_API_KEY", "")
    if not key or key == "replace-with-your-own-key" or any(c.isspace() for c in key):
        raise ValueError("Set MODELFLUX_API_KEY to your own key (see docs/quickstart.md).")
    base = os.environ.get("MODELFLUX_BASE_URL", "https://modelflux.cn/v1").rstrip("/")
    parsed = urllib.parse.urlsplit(base)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("MODELFLUX_BASE_URL must be an HTTPS base URL without credentials, query or fragment.")
    payload = {
        "model": os.environ.get("MODELFLUX_MODEL", "deepseek-flash"),
        "messages": [{"role": "user", "content": "Reply with exactly: ModelFlux connection OK"}],
        "stream": False,
        "max_tokens": 128,
    }
    request = urllib.request.Request(
        base + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.build_opener(NoRedirect()).open(request, timeout=90) as response:
        data = json.load(response)
    if not data.get("choices") or not data["choices"][0].get("message", {}).get("content"):
        raise ValueError("Response has no non-empty choices[0].message.content.")
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as error:
        # Keep arbitrary server error bodies (which may contain private details) out of logs.
        print(f"HTTP {error.code}: check docs/troubleshooting.md and the private console log.", file=sys.stderr)
        sys.exit(1)
    except (urllib.error.URLError, TimeoutError):
        print("Network/TLS/timeout error: check connectivity and certificate trust.", file=sys.stderr)
        sys.exit(1)
    except (ValueError, KeyError, TypeError):
        print("Invalid configuration or response: check environment variables and response format.", file=sys.stderr)
        sys.exit(1)
