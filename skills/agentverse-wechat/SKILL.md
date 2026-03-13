---
name: agentverse-wechat
description: >
  将飞书文档或网页文章排版为特工宇宙（Agent Universe）公众号风格文章。
  完整流程：获取文档 → 生成带样式 HTML → 上传图片到微信 CDN → 注入编辑器 → 设封面/摘要 → 预览。
  Use when: (1) user shares a Feishu doc link or token and wants it published on 公众号,
  (2) user says "排版到公众号" or "发公众号",
  (3) user wants to format an article for WeChat MP editor,
  (4) user mentions "特工宇宙" or "Agent Universe" article formatting.
  Requires: openclaw browser profile, Feishu API access, 公众号 editor access.
---

# AgentVerse WeChat Pipeline v2

将飞书文档排版为公众号文章的完整自动化流程。

> **核心教训**：不要用粘贴（Cmd+V）方式注入内容——ProseMirror 会截断内容并丢失图片。
> **正确方式**：通过微信 API 上传图片获取 CDN URL → 用 innerHTML 注入完整 HTML。

## Style Reference

Read [references/style-guide.md](references/style-guide.md) for complete CSS specs. Key rules:

| 元素 | 样式 |
|------|------|
| 正文 `<p>` | font-size: 15px, line-height: 2em, letter-spacing: 1px, text-align: justify, margin: 0 8px 24px 8px |
| 标题 `<h2>` | font-size: 20px, text-align: center, margin: 32px 8px |
| 题图 | width: 100%, margin: 0, border-radius: 0 |
| 内容图片 | max-width: 100%, margin: 0 8px, border-radius: 4px, **无 margin-bottom** |
| 分隔图 | max-width: 100%, margin: 32px 8px |
| 引用 `""` | 只用中文弯引号，不用 `「」` |

**⚠️ font-size 和 letter-spacing 必须放在 `<p>` 上，不能只放 `<span>`**——公众号编辑器粘贴时会剥离 span 上的这些属性。

---

## Pipeline Steps（共 6 步）

### Step 1: 获取文档 + 下载图片

```
feishu_fetch_doc(doc_id=<token_or_url>)
```

获取 Markdown 内容，记录所有图片 token（如 `ECqTbC2gVo...`）。

**下载图片**：用 `feishu_drive_fetch_media` API 逐张下载到工作目录：

```
mkdir -p ~/.openclaw/workspace-dev/<article-slug>/
feishu_drive_fetch_media(resource_token=<img_token>, type="media", output_path="<workdir>/img_<N>.png")
```

> **备选方案**：如果 API 无权限，可在浏览器打开飞书文档页面，用 `fetch(url, {credentials:'include'})` 方式下载。

### Step 2: 生成带样式 HTML

写 Python 脚本生成 `article.html`，图片位置用 `IMG_PLACEHOLDER_N`。

**⚠️ 占位符替换时必须倒序（16→1）**，否则 `IMG_PLACEHOLDER_1` 会匹配到 `IMG_PLACEHOLDER_10` 中的 `1`。

HTML 结构：
```html
<html lang="zh-CN"><head><meta charset="UTF-8"></head>
<body style="max-width: 680px; margin: 0 auto; padding: 20px; background: #fff;">
  <!-- 题图：全宽，无边距，无段后距 -->
  <div style="text-align: center; margin-left: 0; margin-right: 0;">
    <img src="IMG_PLACEHOLDER_1" style="width: 100%; border-radius: 0;" />
  </div>
  <!-- 正文段落 -->
  <p style="line-height: 2em; font-size: 15px; letter-spacing: 1px; margin-bottom: 24px; margin-left: 8px; margin-right: 8px; text-align: justify;">
    <span style="color: rgb(30,30,30); font-size: 15px; letter-spacing: 1px;">文字内容</span>
  </p>
  <!-- 标题 -->
  <h2 style="text-align: center; margin: 32px 8px;"><span style="font-size: 20px;"><b>标题</b></span></h2>
  <!-- 内容图片：无段后距，紧贴下方内容 -->
  <div style="text-align: center; margin-left: 8px; margin-right: 8px;">
    <img src="IMG_PLACEHOLDER_N" style="max-width: 100%; border-radius: 4px;" />
  </div>
</body></html>
```

**⚠️ 用 `<div>` 不要用 `<section>`**——`<section>` 在 innerHTML 注入时兼容性更好。

### Step 3: 修复排版

```bash
python3 <skill-dir>/scripts/fix_typography.py article.html
```

处理：直引号→弯引号、中英文间距。

### Step 4: 上传图片到微信 CDN + 生成最终 HTML

这是**关键步骤**。不要试图用 base64 内嵌或 localhost URL——必须上传到微信 CDN。

#### 4a. 打开公众号后台

```
browser(action="open", profile="openclaw", targetUrl="https://mp.weixin.qq.com")
```

确认已登录，从 URL 中提取 `token=xxx`。

#### 4b. 创建新文章

点击"图文消息"或"文章"进入编辑器，获取编辑器 tab 的 `targetId`。

#### 4c. 上传图片

用 Node.js 通过 CDP 在编辑器页面的上下文中调用微信文件上传 API：

```javascript
// 上传单张图片到微信 CDN
const fd = new FormData();
const blob = new Blob([imageArrayBuffer], {type: 'image/png'});
fd.append('file', blob, 'img_1.png');

const r = await fetch('/cgi-bin/filetransfer?action=upload_material&f=json&scene=1&writetype=doublewrite&groupid=1&token=<TOKEN>&lang=zh_CN', {
  method: 'POST',
  body: fd,
  credentials: 'include'
});
const data = await r.json();
// data.cdn_url 或 data.url 即为微信 CDN 地址
```

**完整上传脚本** `upload_and_inject.js`（见 scripts/ 目录）：
1. 读取所有本地图片文件
2. 逐张上传到微信 CDN，收集 URL 映射
3. 读取 article.html，**倒序**替换 `IMG_PLACEHOLDER_N` 为 CDN URL
4. 通过 `innerHTML` 注入到 ProseMirror 编辑器

#### 4d. 注入 HTML 到编辑器

通过 CDP 直接设置 ProseMirror 的 innerHTML：

```javascript
var pm = document.querySelector(".ProseMirror");
pm.innerHTML = htmlContent;  // 包含微信 CDN 图片 URL 的完整 HTML
pm.dispatchEvent(new Event("input", {bubbles: true}));
```

> **⚠️ 绝对不要用 Cmd+V 粘贴方式**——ProseMirror 粘贴处理会：
> - 截断内容（4300 字变 2200 字）
> - 丢失第一个 `<section>` 元素
> - 不稳定，每次截断位置不同
>
> innerHTML 注入 100% 可靠，内容完整。

### Step 5: 设置标题 + 封面 + 摘要

**设置标题**（在注入内容之前或之后都可以）：
```javascript
var ta = document.querySelector('#title');
var setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
setter.call(ta, '文章标题');
ta.dispatchEvent(new Event('input', {bubbles: true}));
ta.dispatchEvent(new Event('change', {bubbles: true}));
```

**设置封面**：
1. 点击 `.js_selectCoverFromContent`
2. 等 2 秒，点击第一个 `.appmsg_content_img_item`
3. 点击"下一步"（`.weui-desktop-btn_primary` + `offsetHeight > 0` + 文本含"下一步"）
4. 点击"确认"

**设置摘要**（≤15 字，必须有标点结尾）：
```javascript
var ta = document.querySelector('#js_description');
var setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
setter.call(ta, '摘要内容。');
ta.dispatchEvent(new Event('input', {bubbles: true}));
```

### Step 6: 保存 + 预览

1. 点击 `#js_submit` 保存草稿
2. 等 5 秒
3. 点击"预览"按钮
4. 等 3 秒
5. 在 `.wechat_send_dialog .dialog_ft` 中点击"确定"

```javascript
var ft = document.querySelector('.wechat_send_dialog .dialog_ft');
ft.querySelector('a, button').click();
```

---

## 关键脚本

### scripts/upload_and_inject.js

一站式脚本：上传图片 + 替换 URL + 注入编辑器。

```bash
node <skill-dir>/scripts/upload_and_inject.js \
  --ws <cdp-websocket-url> \
  --token <weixin-token> \
  --html article.html \
  --images img_1.png img_2.png ... img_16.png
```

### scripts/fix_typography.py

排版修复：直引号→弯引号，中英文间距。

### scripts/extract_images.js

（保留，但不推荐用于新流程）从浏览器页面提取 base64 图片。

---

## 强制检查清单（每次排版必须逐项验证）

### 生成 HTML 后
- [ ] H2 font-size 是 20px？（不是 16px、18px、24px）
- [ ] 正文 p font-size 是 15px、letter-spacing 1px、line-height 2em？
- [ ] font-size 和 letter-spacing 放在 `<p>` 上了？（不能只放 span）
- [ ] text-align: justify 放在 `<p>` 上了？
- [ ] 题图 margin-left/right 是 0？border-radius 是 0？
- [ ] 内容图片 margin 8px、border-radius 4px？
- [ ] 用的是 `<div>` 不是 `<section>`？
- [ ] 引号全是中文弯引号 `""`？
- [ ] 图片容器 `<div>` 没有 margin-bottom？（图片不带段后距）
- [ ] 首段文字与原文一致？（打印前 60 字验证）

### 上传图片后
- [ ] 16 张（或 N 张）全部返回 cdn_url？
- [ ] 占位符**倒序**替换（N→1）？

### 注入编辑器后
- [ ] textContent 长度 > 4000？（不是 2243 这种截断值）
- [ ] 首段文字与原文一致？
- [ ] img 数量 = 原文图片数量？
- [ ] 截图肉眼确认排版正确？

### 保存预览后
- [ ] 标题已设置？
- [ ] 封面已选择？
- [ ] 摘要 ≤15 字且有标点结尾？

> **规则：任何一项不通过，立即停下修复，不要继续下一步。**

---

## 踩坑记录（血泪教训）

### ❌ 不要用 Cmd+V 粘贴
ProseMirror 粘贴会截断内容、丢失元素。用 innerHTML 注入。

### ❌ 不要用 base64 data URI 作为 img src
微信编辑器不认 base64 图片，必须上传到微信 CDN 获取 `mmbiz.qpic.cn` URL。

### ❌ 不要用 localhost URL 作为 img src
编辑器无法访问 localhost，保存后图片会丢失。

### ❌ 占位符替换不要正序
`IMG_PLACEHOLDER_1` 会把 `IMG_PLACEHOLDER_10` 里的 `1` 也替换掉。**必须倒序替换**（16→1）。

### ❌ 不要假设端口空闲
旧的 HTTP 服务进程可能占用端口。启动前先 `pkill -f "http.server <port>"` 或换端口。

### ❌ 不要用 `/cgi-bin/uploadimg2cdn` 上传图片
这个端点返回 `errcode: -1`。正确的端点是 `/cgi-bin/filetransfer?action=upload_material`。

### ✅ 每步都要验证
- 生成 HTML 后检查首段文字是否正确
- 上传图片后检查返回的 CDN URL 是否有效
- 注入后检查 textContent 长度和首段文字
- 保存后截图确认排版

### ✅ 同一方法失败 2 次就换策略
不要反复重试同一个不工作的方法。

---

## 完整流程耗时参考

| 步骤 | 预计耗时 |
|------|---------|
| 获取文档 + 下载图片 | 1-2 分钟 |
| 生成 HTML + 修复排版 | 30 秒 |
| 上传图片到微信 CDN | 1-2 分钟 |
| 注入编辑器 + 设置元信息 | 30 秒 |
| 保存 + 预览 | 30 秒 |
| **总计** | **3-5 分钟** |

---

## Gotchas（保留）

### Font Size & Letter Spacing
`font-size: 15px` 和 `letter-spacing: 1px` 必须放在 `<p>` 上。公众号编辑器会剥离 `<span>` 上的这些属性。

### Title Field
`#title` 是 `<textarea>`，必须用 `Object.getOwnPropertyDescriptor` 方式设值。

### Preview Dialog
多个 dialog 可能同时存在，用 `offsetHeight > 0` 过滤可见的。
