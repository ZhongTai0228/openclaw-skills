#!/usr/bin/env node
/**
 * Extract base64 images from a browser page via Chrome DevTools Protocol.
 *
 * The target page must already have window._img_b64_1 ... window._img_b64_N
 * populated (via fetch+FileReader injection).
 *
 * Usage:
 *   node extract_images.js <ws-url> <template.html> <output.html> <image-count>
 *
 * The template HTML must contain IMG_PLACEHOLDER_1 ... IMG_PLACEHOLDER_N.
 */
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

const [,, wsUrl, templatePath, outputPath, countStr] = process.argv;
const imageCount = parseInt(countStr, 10);

if (!wsUrl || !templatePath || !outputPath || !imageCount) {
  console.error('Usage: node extract_images.js <ws-url> <template.html> <output.html> <image-count>');
  process.exit(1);
}

async function run() {
  const ws = new WebSocket(wsUrl);
  let id = 1;
  const pending = {};

  ws.on('message', data => {
    const msg = JSON.parse(data);
    if (msg.id && pending[msg.id]) pending[msg.id](msg.result);
  });

  function send(method, params) {
    return new Promise((resolve, reject) => {
      const myId = id++;
      pending[myId] = resolve;
      ws.send(JSON.stringify({ id: myId, method, params }));
      setTimeout(() => reject(new Error(`Timeout on call ${myId}`)), 30000);
    });
  }

  await new Promise(r => ws.on('open', r));

  // First check if extraction is complete
  const statusResult = await send('Runtime.evaluate', {
    expression: `JSON.stringify({done: window._imgDone, total: window._imgTotal})`,
    returnByValue: true
  });
  const status = JSON.parse(statusResult?.result?.value || '{}');
  if (status.done !== status.total) {
    console.warn(`Warning: only ${status.done}/${status.total} images extracted. Proceeding anyway.`);
  }

  let html = fs.readFileSync(templatePath, 'utf8');
  let missing = 0;

  for (let i = 1; i <= imageCount; i++) {
    process.stdout.write(`Extracting image ${i}/${imageCount}...`);
    const result = await send('Runtime.evaluate', {
      expression: `window._img_b64_${i}`,
      returnByValue: true
    });
    const b64 = result?.result?.value;
    if (!b64) { console.log(' MISSING!'); missing++; continue; }
    console.log(` ${(b64.length / 1024).toFixed(0)} KB`);
    html = html.replace(`IMG_PLACEHOLDER_${i}`, b64);
  }

  fs.writeFileSync(outputPath, html);
  const sizeMB = (html.length / 1024 / 1024).toFixed(1);
  console.log(`\nDone! Written to ${outputPath} (${sizeMB} MB)`);
  if (missing > 0) console.warn(`⚠️ ${missing} images were missing!`);
  ws.close();
}

run().catch(e => { console.error(e); process.exit(1); });
