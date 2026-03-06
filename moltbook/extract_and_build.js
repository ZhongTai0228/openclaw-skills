const http = require('http');
const fs = require('fs');
const WebSocket = require('ws');

const CDP_PORT = 19012;
const TARGET_ID = '5BAA75A1612C81E4C9D1621E32E511E2';

async function main() {
  const targets = await new Promise((resolve, reject) => {
    http.get(`http://127.0.0.1:${CDP_PORT}/json`, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });

  const target = targets.find(t => t.id === TARGET_ID);
  if (!target) { console.error('Target not found'); process.exit(1); }

  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise(r => ws.on('open', r));

  let msgId = 0;
  function evaluate(expr) {
    return new Promise((resolve, reject) => {
      const id = ++msgId;
      ws.send(JSON.stringify({
        id,
        method: 'Runtime.evaluate',
        params: { expression: expr, returnByValue: true }
      }));
      ws.on('message', function handler(raw) {
        const msg = JSON.parse(raw);
        if (msg.id === id) {
          ws.removeListener('message', handler);
          if (msg.result?.result?.value !== undefined) resolve(msg.result.result.value);
          else reject(new Error(JSON.stringify(msg)));
        }
      });
    });
  }

  let html = fs.readFileSync(__dirname + '/article.html', 'utf8');

  for (let i = 1; i <= 15; i++) {
    console.log(`Extracting image ${i}...`);
    const b64 = await evaluate(`window._img_b64_${i}`);
    html = html.replace(`IMG_PLACEHOLDER_${i}`, b64);
    console.log(`  Image ${i}: ${b64.length} chars`);
  }

  const outPath = __dirname + '/article_final.html';
  fs.writeFileSync(outPath, html, 'utf8');
  console.log(`\nDone! Written to ${outPath}`);
  console.log(`Size: ${(fs.statSync(outPath).size / 1024).toFixed(1)} KB`);

  ws.close();
}

main().catch(e => { console.error(e); process.exit(1); });
