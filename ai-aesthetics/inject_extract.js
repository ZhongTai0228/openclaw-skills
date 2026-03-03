const WebSocket = require('ws');
const fs = require('fs');

const wsUrl = process.argv[2];
const htmlFile = process.argv[3];
const outputFile = process.argv[4];
const imgCount = parseInt(process.argv[5]);

const tokens = [
  'TlHQbqTgJoUspQxpAhccp2sFnKe','GfJ0bcoQIo3qmlxoebRcZFnlnQf',
  'HCBkbO8PLoG3g5x871xcgTt2nef','SeG4b6JTPoUGwhx2ctpcOXe2nZx',
  'PzDKblDnmonhbCxWOEhcMOxmnDh','PSnlbGgXzolDT1xKq7Ac0N1UnXg',
  'QeAPbAnFEoE9flxSHEEcTG9sn3c','ZztTbvnkKo3IOLxuwjNcpYu1nyb',
  'RzqFbVKDGosL0FxnkABcAOxXnWd','Wp3cbEa7ro5lofxyh1Zcn0vDnSf',
  'R5RKbWolWowaRYxJrRUc7KHMn6e','F7OBbo17Soku1bxAGB5c1AUintc',
  'NO1bbyYnWoedBzx9eiQceTRbn2f','MkddbF4rIox04kxpbM5cEuB6nFe',
  'Fq4bbkn22o6EbWxK3t8cdxHRnMf','ORKyb79CAoocO5xTab3cUA9qnce',
  'XyAIbFCZDojxa2x5wvTcbiKJn8d','Pw0rbTqWXoBX0dxDwTccpmhFne8',
  'Ss9SbYiYEoM3IAxvYt6ceBl6noh','LlA7bw5qXoQxctxAbk9chT6BnOd',
  'FnhmbndXYoLwX5xTrmpc0Rmanbf','UecpbbVGTo0DarxgBxUcg0L3nzh',
  'PtZ1bB1LwokHfQxbcY6c4Rt8nkc','TGwLbaFuZobKfcx5V5acbotWnwc',
  'D0odb8s96o0raoxU92EcShRBnrb','X51NbSHMtoiz83xV1BhcCxUjn5c'
];

async function main() {
  const ws = new WebSocket(wsUrl);
  let msgId = 0;
  const pending = {};

  ws.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    if (msg.id && pending[msg.id]) {
      pending[msg.id](msg);
    }
  });

  function send(method, params) {
    return new Promise((resolve) => {
      const id = ++msgId;
      pending[id] = resolve;
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  await new Promise(r => ws.on('open', r));

  // Inject extraction script
  const injectScript = `
    (async () => {
      const tokens = ${JSON.stringify(tokens)};
      window._imgDone = 0;
      window._imgTotal = tokens.length;
      for (let i = 0; i < tokens.length; i++) {
        try {
          const url = 'https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/v2/cover/' + tokens[i] + '/?fallback_source=1&height=2000&mount_node_token=I1OtwVKgvikPFPkWn2Lczhmjn5b&mount_point=wiki_image&policy=equal';
          const resp = await fetch(url, {credentials: 'include'});
          const blob = await resp.blob();
          const reader = new FileReader();
          const b64 = await new Promise(resolve => {
            reader.onload = () => resolve(reader.result);
            reader.readAsDataURL(blob);
          });
          window['_img_b64_' + (i + 1)] = b64;
        } catch (e) {
          window['_img_b64_' + (i + 1)] = null;
        }
        window._imgDone++;
      }
      return window._imgDone;
    })()
  `;

  console.log('Injecting image extraction script...');
  const injectResult = await send('Runtime.evaluate', {
    expression: injectScript,
    awaitPromise: true,
    returnByValue: true
  });
  console.log('Extraction done:', injectResult.result?.result?.value);

  // Now pull each image and replace placeholders
  let html = fs.readFileSync(htmlFile, 'utf-8');
  let replaced = 0;

  for (let i = 1; i <= imgCount; i++) {
    const getB64 = await send('Runtime.evaluate', {
      expression: `window._img_b64_${i}`,
      returnByValue: true
    });
    const b64 = getB64.result?.result?.value;
    if (b64) {
      html = html.replace(`IMG_PLACEHOLDER_${i}`, b64);
      replaced++;
      console.log(`Image ${i}/${imgCount}: OK (${b64.length} chars)`);
    } else {
      console.log(`Image ${i}/${imgCount}: FAILED`);
    }
  }

  fs.writeFileSync(outputFile, html, 'utf-8');
  console.log(`Done! Replaced ${replaced}/${imgCount} images. Output: ${outputFile}`);
  ws.close();
}

main().catch(e => { console.error(e); process.exit(1); });
