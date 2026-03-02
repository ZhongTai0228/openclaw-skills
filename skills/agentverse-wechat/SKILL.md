---
name: agentverse-wechat
description: >
  Convert Feishu wiki documents into formatted WeChat 公众号 articles (观猹笔记 style).
  Full pipeline: fetch doc → generate styled HTML → extract images as base64 → paste into 公众号 editor → set cover/summary → preview.
  Use when: (1) user shares a Feishu doc link or token and wants it published on 公众号,
  (2) user says "排版到公众号" or "发公众号",
  (3) user wants to format an article for WeChat MP editor,
  (4) user mentions "Agent Universe" article or 观猹笔记 formatting.
  Requires: openclaw browser profile with Chrome DevTools, Feishu API access, 公众号 editor access.
---

# AgentVerse WeChat Pipeline

Convert Feishu wiki docs to styled 公众号 articles. Full workflow below.

## Style Reference

Read [references/style-guide.md](references/style-guide.md) for complete CSS specs. Key rules:

- **Justify** all text except H2 (centered)
- **Chinese curved quotes** `""` only — no straight quotes, no `「」`
- **CJK spacing**: space between Chinese and English/numbers, but NOT before/after Chinese punctuation
- **Hero image**: full-width, no margin, no border-radius
- **Other images**: 8px side margins, 4px border-radius
- **Separator images**: 32px top/bottom margin, identifiable by dimensions (typically 1080×166)
- **Footer images**: bottom branding/QR images, treat as regular content images

## Pipeline Steps

### 1. Fetch Document

```
feishu_fetch_doc(doc_id=<token_or_url>)
```

Get full markdown. Note image tokens (various formats like `Keexbt8BDo...`). Count total images.

**Image classification**: Examine dimensions in the markdown to classify:
- **Hero image**: first image, typically wide aspect ratio (e.g. 1702×920)
- **Separator images**: narrow banners, typically 1080×166
- **Content images**: screenshots/photos, typically ~1790×1200
- **Footer images**: bottom branding, various sizes around 1080×290-343

### 2. Generate Styled HTML

Write a Python script to generate `article.html` with inline CSS per style guide.

**Critical**: Use `IMG_PLACEHOLDER_1` through `IMG_PLACEHOLDER_N` for images (sequential numbering matching image token order).

Structure:
```html
<html lang="zh-CN"><head><meta charset="UTF-8"></head>
<body style="max-width: 680px; margin: 0 auto; padding: 20px; background: #fff;">
  <!-- Hero image: full-width, NO side margins -->
  <section style="text-align: center; margin-bottom: 24px; margin-left: 0; margin-right: 0;">
    <img src="IMG_PLACEHOLDER_1" style="width: 100%; border-radius: 0;" />
  </section>
  <!-- Body paragraphs: justified ON THE P TAG, with side margins -->
  <p style="line-height: 2em; margin-bottom: 24px; margin-left: 8px; margin-right: 8px; text-align: justify;">
    <span style="color: rgb(30,30,30); font-family: 'PingFang SC',system-ui,-apple-system,'Helvetica Neue','Hiragino Sans GB','Microsoft YaHei UI','Microsoft YaHei',Arial,sans-serif; font-size: 15px; letter-spacing: 1px;">
      Text content here
    </span>
  </p>
  <!-- H2: centered, 32px top/bottom margin -->
  <h2 style="text-align: center; line-height: 2em; margin-top: 32px; margin-bottom: 32px; margin-left: 8px; margin-right: 8px;">
    <span style="color: rgb(30,30,30); font-family: ...; font-size: 20px; letter-spacing: 1px;">
      <span style="font-weight: bold;">Title</span>
    </span>
  </h2>
  <!-- Separator image: centered, 32px margin -->
  <section style="text-align: center; margin-top: 32px; margin-bottom: 32px; margin-left: 8px; margin-right: 8px;">
    <img src="IMG_PLACEHOLDER_N" style="max-width: 100%;" />
  </section>
  <!-- Content image: centered, 8px side margins -->
  <section style="text-align: center; margin-bottom: 24px; margin-left: 8px; margin-right: 8px;">
    <img src="IMG_PLACEHOLDER_N" style="max-width: 100%; border-radius: 4px;" />
  </section>
</body></html>
```

### 3. Fix Typography

Run the typography fixer on the HTML source **before** image embedding:

```bash
python3 <skill-dir>/scripts/fix_typography.py article.html
```

This handles: straight quotes → Chinese curved quotes `""`, CJK/Latin spacing rules.

### 4. Extract Images as Base64

**Method: `fetch()` with credentials from the Feishu doc page** (proven reliable).

1. Open the Feishu doc URL in openclaw browser (`browser action=open`)
2. Wait for the page to load (~5 seconds)
3. Inject a single JS snippet that uses `fetch()` with `credentials: 'include'` to download each image by token, convert to base64 via `FileReader.readAsDataURL()`, and store as `window._img_b64_N`:

```javascript
// Inject this into the Feishu doc page
var tokens = ['token1', 'token2', ...]; // all image tokens in order
window._imgDone = 0;
window._imgTotal = tokens.length;
async function extractAll() {
  for (var i = 0; i < tokens.length; i++) {
    try {
      var url = 'https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/v2/cover/'
        + tokens[i] + '/?fallback_source=1&height=2000&mount_node_token=<WIKI_TOKEN>&mount_point=wiki_image&policy=equal';
      var resp = await fetch(url, {credentials: 'include'});
      var blob = await resp.blob();
      var reader = new FileReader();
      var b64 = await new Promise(function(resolve) {
        reader.onload = function() { resolve(reader.result); };
        reader.readAsDataURL(blob);
      });
      window['_img_b64_' + (i + 1)] = b64;
    } catch (e) {
      window['_img_b64_' + (i + 1)] = null;
    }
    window._imgDone++;
  }
}
extractAll();
```

4. Wait ~15 seconds for all images to download (poll `window._imgDone`)
5. Use CDP WebSocket script (`extract_images.js`) to pull values and replace placeholders:

```bash
cd <workdir> && npm install ws  # one-time
node <skill-dir>/scripts/extract_images.js <ws-url> article.html article_final.html <count>
```

**⚠️ DO NOT use `crossOrigin = 'use-credentials'` with `new Image()` + canvas approach** — this fails with CORS errors on the public sharing page. The `fetch()` + `FileReader` approach works because same-origin fetch with credentials is allowed.

**⚠️ The `mount_node_token` in the URL must match the wiki document token** (the part after `/wiki/` in the URL).

### 5. Paste into 公众号 Editor

1. Serve `article_final.html` locally: `python3 -m http.server <port>` (use any free port; check 8899/8900 etc.)
2. Navigate a browser tab to the local URL, wait for load
3. Select all body content and Cmd+C:

```javascript
var c = Array.from(document.body.children);
var r = document.createRange();
r.setStartBefore(c[0]); r.setEndAfter(c[c.length - 1]);
window.getSelection().removeAllRanges(); window.getSelection().addRange(r);
// Then press Meta+C
```

4. Open a **new** 公众号 editor tab: `https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=77&token=<TOKEN>&lang=zh_CN`
5. **Set title FIRST** (before pasting) — it's a `<textarea id="title">`, must use native setter:

```javascript
var ta = document.querySelector('#title');
var setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
setter.call(ta, '文章标题');
ta.dispatchEvent(new Event('input', {bubbles: true}));
ta.dispatchEvent(new Event('change', {bubbles: true}));
```

6. Focus `.ProseMirror` editor and paste (Cmd+V)
7. Wait **15-20 seconds** for images to upload (24 images take time)

### 6. Set Cover Image

1. Click `.js_selectCoverFromContent` to open image picker
2. Click first `.appmsg_content_img_item` to select hero image
3. Click "下一步" button (find via `.weui-desktop-btn_primary` with text "下一步" and `offsetHeight > 0`)
4. In crop dialog, click "确认" button (find visible button with text "确认")
5. Confirm cover is set

### 7. Write Summary (摘要)

Set `#js_description` textarea value using native setter (same pattern as title):

```javascript
var ta = document.querySelector('#js_description');
var setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
setter.call(ta, '摘要内容。');
ta.dispatchEvent(new Event('input', {bubbles: true}));
```

Rules:
- ≤15 characters
- Catchy/attractive
- **Must end with punctuation** (。！？)

### 8. Save & Preview

1. Click `#js_submit` ("保存为草稿")
2. Wait 5 seconds
3. Click "预览" button (find by text content, use `offsetHeight > 0` filter)
4. Wait 3 seconds for dialog
5. Find the "发送预览" dialog — **it uses class `.wechat_send_dialog`**, look for it in all `[class*=dialog]` elements with `offsetHeight > 0`
6. Click the send/confirm button inside `.dialog_ft`:

```javascript
var dialogs = document.querySelectorAll('.wechat_send_dialog');
for (var i = 0; i < dialogs.length; i++) {
  if (dialogs[i].offsetHeight > 0) {
    var ft = dialogs[i].querySelector('.dialog_ft');
    if (ft) ft.querySelector('a, button').click();
  }
}
```

**⚠️ The dialog may appear but NOT be detected by checking `.wechat_send_dialog` class alone** — use a broader `[class*=dialog]` search and look for "发送预览" text content as a backup detection method.

## Gotchas & Lessons Learned

### Text Alignment (Critical!)
- **`text-align: justify` MUST be on `<p>` (block element), NOT on `<span>` (inline element)** — it's completely ignored on inline elements.
- **DO NOT add `word-break: break-all`** — it chops English words mid-word, looks terrible.
- **DO NOT add `overflow-wrap: break-word`** — unnecessary; default behavior already does the right thing.
- The correct behavior: English words that don't fit wrap whole to the next line, and the previous line's Chinese text stretches to fill both edges. This happens automatically with `text-align: justify` on the `<p>`.

### Image Extraction
- **✅ USE `fetch()` + `credentials: 'include'`** from the Feishu doc page. This is the reliable method.
- **❌ DO NOT use `new Image()` + `crossOrigin='use-credentials'` + canvas** — fails with CORS on the `my.feishu.cn` public sharing page.
- **❌ DO NOT try `feishu_drive_fetch_media`** — requires `docs:document.media:download` app scope which may not be available.
- The Feishu page at `my.feishu.cn/wiki/xxx` is a **public sharing page** with watermarks but still allows `fetch()` with credentials for image URLs.
- Image URL pattern: `https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/v2/cover/<TOKEN>/?fallback_source=1&height=2000&mount_node_token=<WIKI_TOKEN>&mount_point=wiki_image&policy=equal`

### Title Field
- `#title` is a `<textarea>`, NOT a contentEditable div.
- Must use `Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set` to set value programmatically.
- **Set title BEFORE saving** — the `default-203` error often means title is empty.
- Must dispatch both `input` and `change` events after setting.

### ProseMirror Editor
- 公众号 uses ProseMirror, editor div is `.ProseMirror`.
- Must call `browser(action="focus")` on the tab before evaluating JS on it.
- After pasting, wait sufficient time for all images to upload to WeChat servers.

### Preview Dialog
- Multiple dialog elements may exist on the page (most hidden).
- The "发送预览" dialog may be detected via `[class*=dialog]` with text containing "发送预览".
- Always filter by `offsetHeight > 0` to find visible dialogs.
- Preview can be sent even if auto-save shows errors — preview is an independent operation.

### Auto-Save Errors
- `default-203` typically means a required field is missing (usually title).
- Auto-save failure does NOT block preview sending.
- If save keeps failing, check: title set? comment/留言 selected?

### Port Conflicts
- Local HTTP server port may be occupied from previous sessions.
- Always check and use a different port if needed (8899, 8900, etc.).

### General
- Create a working directory per article (e.g. `~/.openclaw/workspace-dev/<article-slug>/`).
- Keep the generation script (`generate.py`) for reproducibility.
- The `ws` npm package is needed for CDP communication — install once per working dir.
- Token from 公众号 URL (`token=476910112`) may change across sessions.
