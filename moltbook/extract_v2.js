const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

const WS_URL = 'ws://127.0.0.1:19012/devtools/page/5BAA75A1612C81E4C9D1621E32E511E2';

async function run() {
  const ws = new WebSocket(WS_URL);
  let id = 1;
  const pending = {};

  ws.on('message', data => {
    const msg = JSON.parse(data);
    if (msg.id && pending[msg.id]) {
      pending[msg.id](msg.result);
    }
  });

  function send(method, params) {
    return new Promise(resolve => {
      const myId = id++;
      pending[myId] = resolve;
      ws.send(JSON.stringify({ id: myId, method, params }));
    });
  }

  await new Promise(r => ws.on('open', r));

  let html = fs.readFileSync(path.join(__dirname, 'article_v2.html'), 'utf8');

  for (let i = 1; i <= 15; i++) {
    console.log(`Extracting image ${i}...`);
    const result = await send('Runtime.evaluate', {
      expression: `window._img_b64_${i}`,
      returnByValue: true
    });
    const b64 = result?.result?.value;
    if (!b64) { console.error(`Image ${i} missing!`); continue; }
    console.log(`  Image ${i}: ${b64.length} chars`);
    html = html.replace(`IMG_PLACEHOLDER_${i}`, b64);
  }

  const outPath = path.join(__dirname, 'article_v2_final.html');
  fs.writeFileSync(outPath, html);
  console.log(`Done! Written to ${outPath} (${(html.length/1024).toFixed(1)} KB)`);
  ws.close();
}

run().catch(console.error);
