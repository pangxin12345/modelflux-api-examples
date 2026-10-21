// Node.js 20+ built-in fetch; no npm packages or automatic .env loading.
const key = process.env.MODELFLUX_API_KEY;
if (!key || key === 'replace-with-your-own-key' || /\s/.test(key)) {
  console.error('Set MODELFLUX_API_KEY to your own key (see docs/quickstart.md).');
  process.exit(2);
}

try {
  const base = (process.env.MODELFLUX_BASE_URL || 'https://modelflux.cn/v1').replace(/\/+$/, '');
  const url = new URL(base);
  if (url.protocol !== 'https:' || url.username || url.password || url.search || url.hash) {
    throw new Error('Invalid base URL');
  }
  const response = await fetch(base + '/chat/completions', {
    method: 'POST',
    redirect: 'error',
    signal: AbortSignal.timeout(90_000),
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: process.env.MODELFLUX_MODEL || 'deepseek-flash',
      messages: [{ role: 'user', content: 'Reply with exactly: ModelFlux connection OK' }],
      stream: false,
      max_tokens: 128,
    }),
  });
  if (!response.ok) {
    console.error(`HTTP ${response.status}: check docs/troubleshooting.md and the private console log.`);
    process.exitCode = 1;
  } else {
    const data = await response.json();
    if (!data.choices?.[0]?.message?.content) throw new Error('Missing text response');
    console.log(JSON.stringify(data, null, 2));
  }
} catch {
  console.error('Configuration, network, TLS, timeout or response error: check docs/troubleshooting.md.');
  process.exitCode = 1;
}
