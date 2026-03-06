---
name: ai-topic-scout
description: >
  AI 领域选题雷达，为特工宇宙（Agent Universe）公众号自动扫描信息源、提炼选题建议。
  触发：扫描选题、找选题、topic scout、选题雷达、有什么 AI 新闻值得写、今天有什么热点；
  Heartbeat 9/12/15/18/21 点；创建选题表/初始化选题表。
---

# AI Topic Scout

## 概述

自动扫描海外 AI 信息源（X/Twitter KOL、官方博客、科技媒体、社区、播客），**提炼选题建议**（不是新闻搬运），写入飞书多维表格，并通过飞书私聊通知用户。

## 前置条件

- 飞书用户授权（OAuth）可用
- 信息源列表见 `references/sources.md`

## 工作流程

### Phase 0: 初始化多维表格（仅首次）

检查是否已有选题表。搜索飞书文档：

```
feishu_search_doc_wiki(action="search", query="特工宇宙选题库", filter={doc_types: ["BITABLE"]})
```

如果没有找到，创建新的多维表格：

```
feishu_bitable_app(action="create", name="特工宇宙选题库")
```

然后在默认数据表上配置字段。先获取表列表：

```
feishu_bitable_app_table(action="list", app_token=APP_TOKEN)
```

删除默认字段后，创建以下字段：

| 字段名 | type | property |
|---|---|---|
| 选题标题 | 1 (文本) | - |
| 选题角度 | 1 (文本) | - |
| 为什么值得写 | 1 (文本) | - |
| 参考信息源 | 15 (超链接) | *(省略 property)* |
| 标签 | 4 (多选) | `{options: [{name:"模型"},{name:"产品"},{name:"Agent"},{name:"政策"},{name:"行业"},{name:"融资"},{name:"开源"}]}` |
| 热度 | 3 (单选) | `{options: [{name:"⭐"},{name:"⭐⭐"},{name:"⭐⭐⭐"},{name:"⭐⭐⭐⭐"},{name:"⭐⭐⭐⭐⭐"}]}` |
| 状态 | 3 (单选) | `{options: [{name:"待筛选"},{name:"已选"},{name:"写作中"},{name:"已发布"},{name:"放弃"}]}` |
| 发现时间 | 5 (日期) | `{date_formatter:"yyyy/MM/dd"}` |

**重要**：超链接字段(type=15) 必须完全省略 property 参数，传空对象也会报错。

将 `app_token` 和 `table_id` 记住，后续步骤使用。如果是 heartbeat 触发，从飞书搜索已有的"特工宇宙选题库"获取 token。

### Phase 1: 扫描信息源

使用两层策略：**主力用 `exec curl` 直接抓取结构化 API**，可选用 `web_search` 补充（需要 Brave API Key）。

#### 主力方案：exec curl（无需 API Key）

1. **Hacker News 热门 AI 内容**：
   ```bash
   exec: curl -s "https://hn.algolia.com/api/v1/search_by_date?query=AI+OR+LLM+OR+GPT+OR+Claude+OR+agent&tags=story&hitsPerPage=15&numericFilters=points>10" | python3 -c "import json,sys; d=json.load(sys.stdin); [print(f\"{h['points']}pts | {h['title']} | https://news.ycombinator.com/item?id={h['objectID']}\") for h in d['hits']]"
   ```

2. **Reddit r/MachineLearning 热帖**：
   ```bash
   exec: curl -s -H "User-Agent: TopicScout/1.0" "https://www.reddit.com/r/MachineLearning/hot.json?limit=10" | python3 -c "import json,sys; d=json.load(sys.stdin); [print(f\"{p['data']['score']}pts | {p['data']['title'][:80]} | https://reddit.com{p['data']['permalink']}\") for p in d['data']['children'] if p['data'].get('score',0)>20]"
   ```

3. **Reddit r/LocalLLaMA 热帖**（开源动态）：
   ```bash
   exec: curl -s -H "User-Agent: TopicScout/1.0" "https://www.reddit.com/r/LocalLLaMA/hot.json?limit=10" | python3 -c "import json,sys; d=json.load(sys.stdin); [print(f\"{p['data']['score']}pts | {p['data']['title'][:80]} | https://reddit.com{p['data']['permalink']}\") for p in d['data']['children'] if p['data'].get('score',0)>20]"
   ```

4. **TechCrunch AI RSS**：
   ```bash
   exec: curl -s "https://techcrunch.com/category/artificial-intelligence/feed/" | python3 -c "
   import xml.etree.ElementTree as ET, sys
   root = ET.parse(sys.stdin).getroot()
   for item in root.findall('.//item')[:8]:
       title = item.find('title').text
       link = item.find('link').text
       print(f'{title} | {link}')
   "
   ```

5. **The Verge AI RSS**：
   ```bash
   exec: curl -s "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml" | python3 -c "
   import xml.etree.ElementTree as ET, sys
   root = ET.parse(sys.stdin).getroot()
   ns = {'atom': 'http://www.w3.org/2005/Atom'}
   for entry in root.findall('.//atom:entry', ns)[:8]:
       title = entry.find('atom:title', ns).text
       link = entry.find('atom:link', ns).get('href')
       print(f'{title} | {link}')
   "
   ```

6. **ArsTechnica AI RSS**：
   ```bash
   exec: curl -s "https://feeds.arstechnica.com/arstechnica/technology-lab" | python3 -c "
   import xml.etree.ElementTree as ET, sys
   root = ET.parse(sys.stdin).getroot()
   for item in root.findall('.//item')[:8]:
       title = item.find('title').text
       link = item.find('link').text
       if any(kw in title.lower() for kw in ['ai','llm','gpt','claude','model','openai','anthropic','google','agent','robot']):
           print(f'{title} | {link}')
   "
   ```

7. **OpenAI / Anthropic / DeepMind 博客**（通过 web_fetch 抓首页）：
   ```
   web_fetch(url="https://openai.com/blog", maxChars=3000)
   web_fetch(url="https://www.anthropic.com/research", maxChars=3000)
   web_fetch(url="https://deepmind.google/discover/blog/", maxChars=3000)
   ```
   如果 web_fetch 被拦截，用 exec curl 替代。

8. **播客最新一期**（RSS）：
   ```bash
   exec: curl -s "https://api.substack.com/feed/podcast/latent-space" | python3 -c "
   import xml.etree.ElementTree as ET, sys
   try:
       root = ET.parse(sys.stdin).getroot()
       for item in root.findall('.//item')[:3]:
           print(f\"{item.find('title').text} | {item.find('link').text}\")
   except: print('feed unavailable')
   "
   ```

#### 可选增强：web_search（需要 Brave API Key）

如果 `web_search` 可用，额外执行：
```
web_search(query="AI breakthrough OR launch 2026", freshness="pd", count=8)
web_search(query="AI agent autonomous tool use", freshness="pd", count=5)
```

对特别重要的 2-3 条结果，用 `web_fetch` 获取详情。

### Phase 2: 提炼选题

**核心原则：不是新闻搬运，是选题策划。**

对收集到的信息，按以下逻辑提炼选题：

1. **找角度**：不要"X 公司发布了 Y"，而是"Y 意味着什么？对谁有影响？趋势是什么？"
2. **找冲突**：技术 vs 伦理？开源 vs 闭源？巨头 vs 创业？
3. **找读者价值**：特工宇宙的读者是 AI 从业者和爱好者，他们关心什么？
4. **合并同类**：多个信息源报道同一事件 → 一个选题，多个参考链接
5. **评估热度**：
   - ⭐⭐⭐⭐⭐：重大发布/突破，全网热议
   - ⭐⭐⭐⭐：重要动态，圈内热议
   - ⭐⭐⭐：值得关注，有一定讨论
   - ⭐⭐：一般动态
   - ⭐：边缘但有趣

选题示例：
- 原始信息："OpenAI releases GPT-5.4 with computer use" → 选题标题："深度解析 GPT-5.4 的 Computer Use 能力——AI 离替代白领还有多远？"，角度："从技术能力到实际应用场景，分析 computer use 的成熟度和局限性"
- 原始信息："Meta open sources Llama 4" → 选题标题："Llama 4 开源：Meta 的 AI 平权运动还是商业阳谋？"，角度："开源策略的商业逻辑，对 OpenAI/Anthropic 的冲击"

### Phase 3: 去重检查

在写入前，检查多维表格中是否已有类似选题：

```
feishu_bitable_app_table_record(action="list", app_token=APP_TOKEN, table_id=TABLE_ID, page_size=50)
```

对比已有选题标题，跳过重复的。

### Phase 4: 写入多维表格

将新选题批量写入：

```
feishu_bitable_app_table_record(
  action="batch_create",
  app_token=APP_TOKEN,
  table_id=TABLE_ID,
  records=[
    {
      fields: {
        "选题标题": "...",
        "选题角度": "...",
        "为什么值得写": "...",
        "参考信息源": {"text": "来源名称", "link": "https://..."},
        "标签": ["模型", "产品"],
        "热度": "⭐⭐⭐⭐",
        "状态": "待筛选",
        "发现时间": 1709222400000
      }
    },
    ...
  ]
)
```

**注意**：发现时间使用当前时间的毫秒时间戳。超链接字段格式为 `{text: "显示文本", link: "URL"}`。

### Phase 5: 通知用户

通过飞书私聊发送选题摘要。使用消息上下文中的 SenderId 作为 receive_id：

```
feishu_im_user_message(
  action="send",
  receive_id_type="open_id",
  receive_id=USER_OPEN_ID,
  msg_type="post",
  content='{
    "zh_cn": {
      "title": "🔍 AI 选题雷达 - 新发现 N 条选题",
      "content": [
        [{"tag": "text", "text": "本轮扫描发现以下选题：\n\n"}],
        [{"tag": "text", "text": "1. 选题标题\n   热度: ⭐⭐⭐⭐ | 标签: 模型\n   角度: ...\n\n"}],
        ...
        [{"tag": "text", "text": "\n📊 "},{"tag": "a", "text": "查看完整选题库", "href": "BITABLE_URL"}]
      ]
    }
  }'
)
```

**安全约束**：heartbeat 触发时可直接发送通知（用户已通过配置 heartbeat 表达了同意）。用户手动触发时，先展示选题摘要，确认后再发送通知。

## Heartbeat 配置

在 `~/.openclaw/workspace-dev/HEARTBEAT.md` 中添加：

```markdown
## AI Topic Scout
- Schedule: 09:00, 12:00, 15:00, 18:00, 21:00 (Asia/Shanghai)
- Action: 运行 ai-topic-scout skill 的完整扫描流程（Phase 1-5）
```

## 注意事项

1. **不要扫描国内媒体**（不要量子位、36氪、机器之心等）
2. **选题要有角度**，不是新闻标题翻译
3. **超链接字段**创建时不传 property
4. **每轮扫描建议产出 3-8 条选题**，质量优先于数量
5. 如果某轮扫描没有发现值得写的选题，通知用户"本轮无新选题"即可
