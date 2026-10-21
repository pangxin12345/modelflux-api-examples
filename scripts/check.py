#!/usr/bin/env python3
"""Offline checks: syntax, configuration rejection, links and accidental secrets."""
import ast
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
errors = []


def check(ok, label):
    print(('PASS ' if ok else 'FAIL ') + label)
    if not ok:
        errors.append(label)


def run(args, env=None):
    return subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True, timeout=15)


for tool in ('bash', 'node', 'python3', 'git'):
    check(shutil.which(tool) is not None, 'runtime available: ' + tool)
if errors:
    sys.exit(1)

check(run(['bash', '-n', 'examples/curl/chat.sh']).returncode == 0, 'Bash syntax')
check(run(['node', '--check', 'examples/node/chat.mjs']).returncode == 0, 'Node syntax')
for path in (ROOT / 'examples/python/chat.py', Path(__file__)):
    try:
        ast.parse(path.read_text())
        check(True, 'Python syntax: ' + str(path.relative_to(ROOT)))
    except SyntaxError:
        check(False, 'Python syntax: ' + str(path.relative_to(ROOT)))

# All these cases must fail before networking. Never reuse an actual key from CI.
commands = [('curl', ['bash', 'examples/curl/chat.sh']),
            ('python', ['python3', 'examples/python/chat.py']),
            ('node', ['node', 'examples/node/chat.mjs'])]
clean = {k: v for k, v in os.environ.items() if not k.startswith('MODELFLUX_')}
for name, command in commands:
    for label, overrides in [('missing key', {}),
                             ('placeholder key', {'MODELFLUX_API_KEY': 'replace-with-your-own-key'}),
                             ('insecure URL', {'MODELFLUX_API_KEY': 'offline-test-key', 'MODELFLUX_BASE_URL': 'http://invalid.example/v1'})]:
        result = run(command, {**clean, **overrides})
        check(result.returncode != 0 and not result.stdout.strip(), name + ' rejects ' + label)

# A fake curl checks argument handling without networking or real credentials.
with tempfile.TemporaryDirectory(prefix='modelflux-offline-') as temporary:
    fake = Path(temporary) / 'curl'
    fake.write_text('''#!/usr/bin/env python3
import json, pathlib, sys
assert "Authorization: Bearer offline-test-key" in sys.stdin.read()
assert not any("offline-test-key" in arg for arg in sys.argv)
assert "https://modelflux.cn/v1/chat/completions" in sys.argv
payload = json.loads(sys.argv[sys.argv.index("--data") + 1])
assert payload["model"] == "deepseek-flash" and payload["stream"] is False
assert payload["max_tokens"] == 128
result = '{"choices":[{"message":{"content":"offline fixture"}}]}'
if "--output" in sys.argv:
    pathlib.Path(sys.argv[sys.argv.index("--output") + 1]).write_text(result)
else:
    print(result)
''')
    fake.chmod(0o700)
    fixture_env = {**clean, 'PATH': temporary + os.pathsep + clean.get('PATH', ''),
                   'MODELFLUX_API_KEY': 'offline-test-key'}
    result = run(['bash', 'examples/curl/chat.sh'], fixture_env)
    check(result.returncode == 0 and 'offline fixture' in result.stdout, 'curl mock success and auth kept out of argv')
    output = Path(temporary) / 'response.json'
    result = run(['bash', 'examples/curl/chat.sh', str(output)], fixture_env)
    check(result.returncode == 0 and output.exists() and not result.stdout.strip(), 'curl mock optional output file')
    for base in ('https://invalid.example/v1?query=1', 'https://user@invalid.example/v1', 'https://invalid.example/v1#fragment'):
        result = run(['bash', 'examples/curl/chat.sh'], {**fixture_env, 'MODELFLUX_BASE_URL': base})
        check(result.returncode != 0 and not result.stdout.strip(), 'curl rejects URL decorations: ' + base)

files = [p for p in ROOT.rglob('*') if p.is_file() and not any(part in {'.git', '.internal', '.seo-cache'} for part in p.relative_to(ROOT).parts)]
broken = []
secret_like = []
for path in files:
    relative = path.relative_to(ROOT)
    if path.is_symlink():
        secret_like.append(str(relative) + ': symlink')
        continue
    if path.name.startswith('.env') and path.name != '.env.example':
        secret_like.append(str(relative) + ': local environment file')
    text = path.read_text(encoding='utf-8')
    if re.search(r'\bsk-[A-Za-z0-9_-]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', text):
        secret_like.append(str(relative) + ': secret-like material')
    if path.suffix == '.json':
        try:
            json.loads(text)
        except ValueError:
            errors.append('Invalid JSON: ' + str(relative))
    if path.suffix == '.md':
        for target in re.findall(r'\]\(([^)]+)\)', text):
            target = target.split('#', 1)[0]
            if not target or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            resolved = (path.parent / unquote(target)).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                broken.append(str(relative) + ': ' + target)
check(not broken, 'relative Markdown links (' + str(len(broken)) + ' broken)')
check(not secret_like, 'no local env files, symlinks, private keys or token-like strings')
check(run(['git', 'check-ignore', '--no-index', '.env']).returncode == 0, '.env ignored by Git')
check(run(['git', 'check-ignore', '--no-index', '.env.example']).returncode == 1, '.env.example remains publishable')
if broken:
    print('\n'.join(broken))
if secret_like:
    print('\n'.join(secret_like))
print(f'Offline checks: {"FAILED" if errors else "PASSED"}; no API requests made.')
sys.exit(bool(errors))
