#!/usr/bin/env node
/**
 * Upload images to WeChat CDN, replace placeholders in HTML, inject into ProseMirror editor.
 *
 * Usage:
 *   node upload_and_inject.js <ws-url> <weixin-token> <article.html> <img1> <img2> ... <imgN>
 *
 * Example:
 *   node upload_and_inject.js "ws://127.0.0.1:19012/devtools/page/XXXXX" "2084327687" article.html img_1.png img_2.png
 *
 * The article.html must contain IMG_PLACEHOLDER_1 ... IMG_PLACEHOLDER_N.
 * Placeholders are replaced in REVERSE order (N→1) to avoid partial matching.
 */
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
if (args.length < 3) {
  console.error('Usage: node upload_and_inject.js <ws-url> <weixin-token> <article.html> <img1> [img2] ...');
  process.exit(1);
}

const [wsUrl, token, htmlPath, ...imagePaths] = args;
const imageCount = imagePaths.length;

async function main() {
  const ws = new WebSocket(wsUrl);
  let id = 1;

  function sendCDP(expr) {
    return new Promise((resolve, reject) => {
      const myId = id++;
      const timeout = setTimeout(() => reject(new Error(`CDP timeout on call ${myId}`)), 60000);
      const handler = (data) => {
        const msg = JSON.parse(data);
        if (msg.id === myId) {
          clearTimeout(timeout);
          ws.removeListener('message', handler);
          resolve(msg.result);
        }
      };
      ws.on('message', handler);
      ws.send(JSON.stringify({
        id: myId,
        method: 'Runtime.evaluate',
        params: { expression: expr, returnByValue: true, awaitPromise: true }
      }));
    });
  }

  await new Promise(r => ws.on('open', r));
  console.log('Connected to CDP\n');

  // Step 1: Upload all images to WeChat CDN
  console.log(`=== Uploading ${imageCount} images to WeChat CDN ===\n`);
  const cdnUrls = {}; // placeholder -> cdn_url

  for (let i = 0; i < imageCount; i++) {
    const filePath = imagePaths[i];
    const fileData = fs.readFileSync(filePath);
    const b64 = fileData.toString('base64');
    const ext = path.extname(filePath).slice(1).toLowerCase();
    const mime = ext === 'png' ? 'image/png' : 'image/jpeg';
    const fname = path.basename(filePath);
    const placeholderIdx = i + 1;

    process.stdout.write(`  [${placeholderIdx}/${imageCount}] ${fname} (${(fileData.length / 1024).toFixed(0)} KB)... `);

    const expr = `
      new Promise(async (resolve) => {
        try {
          const b64 = ${JSON.stringify(b64)};
          const byteStr = atob(b64);
          const ab = new ArrayBuffer(byteStr.length);
          const ia = new Uint8Array(ab);
          for (let j = 0; j < byteStr.length; j++) ia[j] = byteStr.charCodeAt(j);
          const blob = new Blob([ab], {type: '${mime}'});
          const fd = new FormData();
          fd.append('file', blob, '${fname}');
          const r = await fetch('/cgi-bin/filetransfer?action=upload_material&f=json&scene=1&writetype=doublewrite&groupid=1&token=${token}&lang=zh_CN', {
            method: 'POST', body: fd, credentials: 'include'
          });
          const data = await r.json();
          resolve(JSON.stringify(data));
        } catch(e) { resolve(JSON.stringify({error: e.message})); }
      })
    `;

    const result = await sendCDP(expr);
    const val = result?.result?.value || '{}';
    try {
      const parsed = JSON.parse(val);
      const url = parsed.cdn_url || parsed.url;
      if (url) {
        cdnUrls[`IMG_PLACEHOLDER_${placeholderIdx}`] = url;
        console.log(`✅ ${url.substring(0, 60)}...`);
      } else {
        console.log(`❌ ${val.substring(0, 80)}`);
      }
    } catch(e) {
      console.log(`❌ Parse error: ${val.substring(0, 80)}`);
    }
  }

  const uploadedCount = Object.keys(cdnUrls).length;
  console.log(`\n=== Uploaded ${uploadedCount}/${imageCount} images ===\n`);

  if (uploadedCount === 0) {
    console.error('No images uploaded! Aborting.');
    ws.close();
    process.exit(1);
  }

  // Step 2: Read HTML and replace placeholders (REVERSE ORDER to avoid partial matching)
  console.log('=== Replacing placeholders in HTML ===\n');
  let html = fs.readFileSync(htmlPath, 'utf8');

  // Extract body content
  const bodyMatch = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  let body = bodyMatch ? bodyMatch[1].trim() : html;

  // Convert <section> to <div> for better ProseMirror compatibility
  body = body.replace(/<section/g, '<div').replace(/<\/section>/g, '</div>');

  // Replace in REVERSE order (critical!)
  for (let i = imageCount; i >= 1; i--) {
    const placeholder = `IMG_PLACEHOLDER_${i}`;
    const url = cdnUrls[placeholder];
    if (url) {
      body = body.split(placeholder).join(url);
      console.log(`  ${placeholder} → ✅`);
    } else {
      console.log(`  ${placeholder} → ⚠️ no CDN URL, keeping placeholder`);
    }
  }

  // Step 3: Inject into ProseMirror via innerHTML
  console.log('\n=== Injecting into ProseMirror editor ===\n');

  const jsBody = JSON.stringify(body);
  const injectExpr = `(function(){
    var pm = document.querySelector(".ProseMirror");
    if (!pm) return "ERROR: no .ProseMirror found";
    pm.innerHTML = ${jsBody};
    pm.dispatchEvent(new Event("input", {bubbles: true}));
    return pm.textContent.length + " chars, " + pm.querySelectorAll("img").length + " imgs";
  })()`;

  const injectResult = await sendCDP(injectExpr);
  const injectVal = injectResult?.result?.value || 'unknown';
  console.log(`  Result: ${injectVal}`);

  // Save the final HTML with CDN URLs for reference
  const outputPath = htmlPath.replace('.html', '_cdn.html');
  const fullHtml = `<html lang="zh-CN"><head><meta charset="UTF-8"></head><body style="max-width: 680px; margin: 0 auto; padding: 20px; background: #fff;">${body}</body></html>`;
  fs.writeFileSync(outputPath, fullHtml);
  console.log(`\n  Saved CDN version: ${outputPath}`);

  console.log('\n=== Done! ===');
  ws.close();
}

main().catch(e => { console.error(e); process.exit(1); });
