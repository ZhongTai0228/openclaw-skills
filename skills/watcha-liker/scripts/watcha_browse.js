#!/usr/bin/env node
/**
 * watcha_browse.js - 浏览观猹猹馆帖子并执行点赞操作
 * 
 * 用法:
 *   node watcha_browse.js <action> [options]
 * 
 * Actions:
 *   list          列出当前可见帖子
 *   scroll        滚动并列出帖子
 *   like <index>  点赞指定索引的帖子
 *   like-scroll <keywords...>  滚动寻找包含关键词的帖子并点赞
 * 
 * 需要 Chrome 以 --remote-debugging-port=9222 启动
 * 需要全局安装 ws: npm install -g ws
 */

const CDP_URL = process.env.CDP_URL || 'http://127.0.0.1:9222';
const WATCHA_URL = 'https://watcha.cn/square/discuss';

async function getWsUrl() {
  const http = require('http');
  return new Promise((resolve, reject) => {
    http.get(`${CDP_URL}/json/list`, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const tabs = JSON.parse(data);
          const tab = tabs.find(t => t.url.includes('watcha.cn'));
          if (tab) resolve(tab.webSocketDebuggerUrl);
          else reject(new Error('No watcha.cn tab found. Navigate to watcha.cn first.'));
        } catch(e) { reject(e); }
      });
    }).on('error', () => reject(new Error('Cannot connect to Chrome CDP. Ensure Chrome is running with --remote-debugging-port=9222')));
  });
}

async function connect() {
  const WebSocket = require('ws');
  const wsUrl = await getWsUrl();
  return new Promise((resolve) => {
    const ws = new WebSocket(wsUrl);
    let id = 1;
    function send(method, params = {}) {
      return new Promise(r => {
        const i = id++;
        ws.send(JSON.stringify({ id: i, method, params }));
        const h = d => { const m = JSON.parse(d); if (m.id === i) { ws.removeListener('message', h); r(m); } };
        ws.on('message', h);
      });
    }
    ws.on('open', () => resolve({ ws, send }));
  });
}

async function navigateToChaguan(send) {
  const r = await send('Runtime.evaluate', { expression: 'location.href', returnByValue: true });
  if (!r.result.result.value.includes('square/discuss')) {
    await send('Page.navigate', { url: WATCHA_URL });
    await new Promise(r => setTimeout(r, 5000));
  }
}

async function getVisiblePosts(send) {
  const r = await send('Runtime.evaluate', {
    expression: `
      (function(){
        const posts = [];
        for(let y = 80; y < 800; y += 30) {
          const el = document.elementFromPoint(400, y);
          if(el) {
            const text = el.textContent.substring(0, 200);
            if(text.length > 20 && !posts.some(p => p.text === text)) {
              posts.push({y, text});
            }
          }
        }
        const btns = Array.from(document.querySelectorAll('button.outline-button--react'));
        const inView = btns.filter(b => {
          const r = b.getBoundingClientRect();
          return r.y > 50 && r.y < 800 && /^\\\\d+$/.test(b.textContent.trim());
        });
        return JSON.stringify({
          posts: posts.slice(0, 10),
          thumbButtons: inView.map(b => ({
            text: b.textContent.trim(),
            selected: b.className.includes('selected'),
            x: Math.round(b.getBoundingClientRect().x + b.getBoundingClientRect().width/2),
            y: Math.round(b.getBoundingClientRect().y + b.getBoundingClientRect().height/2)
          }))
        });
      })()
    `, returnByValue: true
  });
  return JSON.parse(r.result.result.value);
}

async function clickAt(send, x, y) {
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y });
  await new Promise(r => setTimeout(r, 80));
  await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 });
  await new Promise(r => setTimeout(r, 40));
  await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 });
  await new Promise(r => setTimeout(r, 1200));
}

async function scrollDown(send) {
  await send('Input.dispatchMouseEvent', { type: 'mouseWheel', x: 400, y: 400, deltaX: 0, deltaY: 400 });
  await new Promise(r => setTimeout(r, 700));
}

async function main() {
  const args = process.argv.slice(2);
  const action = args[0] || 'list';

  const { ws, send } = await connect();
  await navigateToChaguan(send);

  if (action === 'list') {
    const { posts, thumbButtons } = await getVisiblePosts(send);
    console.log(JSON.stringify({ posts, thumbButtons }, null, 2));

  } else if (action === 'scroll') {
    const allPosts = [];
    for (let i = 0; i < 15; i++) {
      const { posts, thumbButtons } = await getVisiblePosts(send);
      for (const p of posts) {
        if (!allPosts.some(ap => ap.text.substring(0,50) === p.text.substring(0,50))) {
          allPosts.push({ ...p, step: i, buttons: thumbButtons });
        }
      }
      await scrollDown(send);
    }
    console.log(JSON.stringify(allPosts.map((p, i) => ({
      index: i,
      preview: p.text.substring(0, 100),
      step: p.step
    })), null, 2));

  } else if (action === 'like') {
    // like visible thumb button at given index (0=first post's thumb)
    const idx = parseInt(args[1] || '0');
    const { thumbButtons } = await getVisiblePosts(send);
    if (idx >= thumbButtons.length) {
      console.error(`Only ${thumbButtons.length} thumb buttons visible. Use 'scroll' first.`);
      process.exit(1);
    }
    const btn = thumbButtons[idx];
    if (btn.selected) {
      console.log(JSON.stringify({ status: 'already_liked', button: btn }));
    } else {
      await clickAt(send, btn.x, btn.y);
      // verify
      const after = await getVisiblePosts(send);
      const newBtn = after.thumbButtons[idx];
      console.log(JSON.stringify({ status: newBtn?.selected ? 'liked' : 'failed', before: btn, after: newBtn }));
    }

  } else if (action === 'like-scroll') {
    // Scroll through posts, find ones matching keywords, and like them
    const keywords = args.slice(1);
    if (keywords.length === 0) {
      console.error('Usage: like-scroll <keyword1> [keyword2] ...');
      process.exit(1);
    }

    const liked = [];
    for (let step = 0; step < 30; step++) {
      const r = await send('Runtime.evaluate', {
        expression: `
          (function(){
            const rects = [];
            for(let y = 100; y < 800; y += 50) {
              const el = document.elementFromPoint(400, y);
              if(el) rects.push(el.textContent.substring(0, 150));
            }
            const visibleText = rects.join(' ');
            const btns = Array.from(document.querySelectorAll('button.outline-button--react'));
            const inView = btns.filter(b => {
              const r = b.getBoundingClientRect();
              return r.y > 100 && r.y < 800 && /^\\\\d+$/.test(b.textContent.trim());
            });
            return JSON.stringify({
              visibleText: visibleText.substring(0, 300),
              btns: inView.map(b => ({
                text: b.textContent.trim(),
                selected: b.className.includes('selected'),
                x: Math.round(b.getBoundingClientRect().x + b.getBoundingClientRect().width / 2),
                y: Math.round(b.getBoundingClientRect().y + b.getBoundingClientRect().height / 2)
              }))
            });
          })()
        `, returnByValue: true
      });
      const info = JSON.parse(r.result.result.value);

      for (const kw of keywords) {
        if (info.visibleText.includes(kw) && info.btns.length > 0) {
          const btn = info.btns[0];
          if (!btn.selected && !liked.some(l => l.keyword === kw)) {
            await clickAt(send, btn.x, btn.y);
            liked.push({ keyword: kw, step, button: btn });
            console.error(`Liked post containing "${kw}" at step ${step}`);
          }
        }
      }

      await scrollDown(send);
      if (liked.length >= keywords.length) break;
    }

    console.log(JSON.stringify({ liked, total: liked.length }));
  }

  ws.close();
  process.exit(0);
}

main().catch(e => { console.error(e.message); process.exit(1); });
