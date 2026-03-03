---
name: watcha-liker
description: >
  Browse and like posts on watcha.cn (观猹) community forum (猹馆).
  Use when: user asks to browse watcha.cn, like/upvote posts on 观猹/猹馆,
  interact with watcha.cn content, or scroll through 猹馆 discussions.
  Requires Chrome with CDP debugging port (9222) and the `ws` npm package.
---

# 观猹猹馆浏览与点赞

Browse the 猹馆 (discussion forum) on watcha.cn and like quality posts via Chrome DevTools Protocol.

## Prerequisites

1. **Chrome with CDP port**: Chrome must run with `--remote-debugging-port=9222` and a non-default `--user-data-dir`.
2. **ws package**: `npm install -g ws`
3. **Logged in**: User must be logged into watcha.cn in the CDP-enabled Chrome.

If Chrome is not running with CDP, run the setup script:

```bash
bash scripts/ensure_chrome_cdp.sh
```

⚠️ This launches Chrome with a fresh profile. User must log in to watcha.cn manually before liking posts.

## Workflow

### 1. Ensure Chrome CDP is available

```bash
curl -s http://127.0.0.1:9222/json/version
```

If this fails, run `scripts/ensure_chrome_cdp.sh`.

### 2. Browse posts

List visible posts:
```bash
NODE_PATH=$(npm root -g) node scripts/watcha_browse.js list
```

Scroll and collect posts:
```bash
NODE_PATH=$(npm root -g) node scripts/watcha_browse.js scroll
```

### 3. Like posts

Like the first visible post's thumb button:
```bash
NODE_PATH=$(npm root -g) node scripts/watcha_browse.js like 0
```

Like posts by keyword (scrolls to find matching posts):
```bash
NODE_PATH=$(npm root -g) node scripts/watcha_browse.js like-scroll "Claude Code" "老歪"
```

## How it works

- Connects to Chrome via CDP WebSocket
- Navigates to `watcha.cn/square/discuss` if not already there
- Uses `document.elementFromPoint()` to detect visible posts (handles virtual list rendering)
- Uses `Input.dispatchMouseEvent` for real mouse clicks (required for the Vue app's event handlers)
- Scrolls with `mouseWheel` events to load more posts
- Verifies like state via button CSS class (`outline-button--selected`)

## Key constraints

- watcha.cn uses **virtual list rendering** — only visible posts exist in DOM
- `window.scrollBy` does not reliably trigger virtual list updates; use `mouseWheel` events
- `document.body.innerText` may not reflect viewport content; use `elementFromPoint` sampling
- Thumb buttons use class `outline-button--react`; selected state uses `outline-button--selected`
- Each post has paired 👍/👎 buttons; filter by `/^\d+$/` text to isolate them from emoji/share buttons
