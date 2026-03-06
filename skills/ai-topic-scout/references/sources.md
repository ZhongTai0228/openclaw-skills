# AI Topic Scout - 信息源清单

> 最后更新：2026-03-07
> 共计 ~50 个信息源，分 8 大类

---

## 1. 科技媒体（RSS + Brave Search）

| 来源 | 方式 | 优先级 |
|---|---|---|
| TechCrunch AI | RSS `techcrunch.com/category/artificial-intelligence/feed/` | ⭐⭐⭐⭐⭐ |
| The Verge AI | RSS Atom Feed | ⭐⭐⭐⭐⭐ |
| Ars Technica | RSS + 关键词过滤 | ⭐⭐⭐⭐ |
| MIT Technology Review | Brave `site:technologyreview.com AI` | ⭐⭐⭐⭐ |
| The Information | Brave `site:theinformation.com AI` | ⭐⭐⭐⭐ |
| Bloomberg AI | Brave `bloomberg.com AI` | ⭐⭐⭐⭐ |
| 404 Media | Brave `site:404media.co AI` | ⭐⭐⭐ |
| Wired AI | Brave `site:wired.com artificial intelligence` | ⭐⭐⭐ |
| CNBC AI | Brave `site:cnbc.com AI` | ⭐⭐⭐ |

## 2. 官方博客（Brave Search site: 搜索）

| 来源 | 搜索查询 | 优先级 |
|---|---|---|
| OpenAI Blog | `site:openai.com/blog` | ⭐⭐⭐⭐⭐ |
| Anthropic | `site:anthropic.com` | ⭐⭐⭐⭐⭐ |
| Google DeepMind | `site:deepmind.google` | ⭐⭐⭐⭐⭐ |
| Google AI Blog | `site:blog.google/technology/ai` | ⭐⭐⭐⭐ |
| Meta AI Blog | `site:ai.meta.com/blog` | ⭐⭐⭐⭐ |
| Mistral | `site:mistral.ai/news` | ⭐⭐⭐⭐ |
| Microsoft AI Blog | `site:blogs.microsoft.com AI` | ⭐⭐⭐ |
| NVIDIA AI Blog | `site:blogs.nvidia.com AI` | ⭐⭐⭐ |
| Apple ML Research | `site:machinelearning.apple.com` | ⭐⭐⭐ |
| Cohere | `site:cohere.com/blog` | ⭐⭐ |

## 3. X/Twitter KOL（Brave Search）

搜索模板：`site:x.com "KOL名" AI` 或 `from:handle AI`

| KOL | Handle | 身份 | 优先级 |
|---|---|---|---|
| Sam Altman | @sama | OpenAI CEO | ⭐⭐⭐⭐⭐ |
| Andrej Karpathy | @karpathy | 前 OpenAI/Tesla，独立研究者 | ⭐⭐⭐⭐⭐ |
| Yann LeCun | @ylecun | Meta AI 首席科学家 | ⭐⭐⭐⭐⭐ |
| Anthropic | @AnthropicAI | Anthropic 官方 | ⭐⭐⭐⭐⭐ |
| Simon Willison | @simonw | AI 工具链/开源意见领袖 | ⭐⭐⭐⭐⭐ |
| Jim Fan | @DrJimFan | NVIDIA 高级研究科学家 | ⭐⭐⭐⭐ |
| Clem Delangue | @ClementDelangue | Hugging Face CEO | ⭐⭐⭐⭐ |
| Ethan Mollick | @emollick | 沃顿商学院教授，AI 应用研究 | ⭐⭐⭐⭐ |
| swyx | @swyx | Latent Space 主播，AI 工程圈核心 | ⭐⭐⭐⭐ |
| Arav Srinivas | @AravSrinivas | Perplexity CEO | ⭐⭐⭐ |
| Bindu Reddy | @bindureddy | Abacus.AI CEO，模型评测 | ⭐⭐⭐ |

## 4. 社区论坛（Curl API 直接抓取）

| 来源 | 方式 | 优先级 |
|---|---|---|
| Hacker News | Algolia API `hn.algolia.com/api/v1/search_by_date` | ⭐⭐⭐⭐⭐ |
| Reddit r/MachineLearning | JSON API `/hot.json` | ⭐⭐⭐⭐⭐ |
| Reddit r/LocalLLaMA | JSON API `/hot.json` | ⭐⭐⭐⭐⭐ |
| Reddit r/ChatGPT | JSON API `/hot.json` | ⭐⭐⭐⭐ |
| Reddit r/singularity | JSON API `/hot.json` | ⭐⭐⭐ |

## 5. 开源/开发者平台（Curl + Brave Search）

| 来源 | 方式 | 优先级 |
|---|---|---|
| Hugging Face Trending Models | curl `huggingface.co/api/models?sort=trending&limit=10` | ⭐⭐⭐⭐⭐ |
| GitHub Trending | curl `github.com/trending?since=daily` + 过滤 AI 相关 | ⭐⭐⭐⭐ |
| ArXiv cs.AI | RSS `arxiv.org/rss/cs.AI` | ⭐⭐⭐⭐ |
| ArXiv cs.CL | RSS `arxiv.org/rss/cs.CL` | ⭐⭐⭐⭐ |
| Papers With Code | Brave `site:paperswithcode.com trending` | ⭐⭐⭐ |

## 6. 播客（RSS + Brave Search）

| 播客 | 方式 | 优先级 |
|---|---|---|
| Latent Space | RSS `api.substack.com/feed/podcast/latent-space` | ⭐⭐⭐⭐⭐ |
| Lex Fridman | Brave `Lex Fridman podcast AI latest` | ⭐⭐⭐⭐ |
| Cognitive Revolution | Brave `cognitive revolution podcast AI latest` | ⭐⭐⭐ |
| Last Week in AI | Brave `last week in AI podcast latest` | ⭐⭐⭐ |
| NVIDIA AI Podcast | Brave `NVIDIA AI podcast latest episode` | ⭐⭐ |

## 7. 综合搜索查询（Brave Search，freshness="pd"）

每轮扫描执行以下查询，限定 24 小时内：

| # | 查询 | 覆盖范围 |
|---|---|---|
| 1 | `AI breakthrough OR AI launch OR AI release today 2026` | 综合热点 |
| 2 | `new AI model release GPT Claude Gemini Llama` | 模型发布 |
| 3 | `AI product launch startup funding 2026` | 产品/融资 |
| 4 | `open source AI model release huggingface` | 开源动态 |
| 5 | `AI regulation policy government` | 政策法规 |
| 6 | `AI agent autonomous tool use` | Agent/应用 |
| 7 | `AI impact industry enterprise adoption` | 行业影响 |

## 8. 数据/榜单（Brave Search，按需）

| 来源 | 搜索查询 | 用途 |
|---|---|---|
| LMSYS Chatbot Arena | `site:chat.lmsys.org leaderboard` | 模型排名变动 |
| Stanford HAI AI Index | `site:aiindex.stanford.edu` | 年度报告/权威数据 |

---

## 扫描优先级说明

- ⭐⭐⭐⭐⭐：每轮必扫，核心信息源
- ⭐⭐⭐⭐：每轮扫描，重要补充
- ⭐⭐⭐：选择性扫描，避免信息过载
- ⭐⭐：低频扫描，特定话题时启用

## 不扫描的源（排除列表）

- ❌ 国内媒体（量子位、36氪、机器之心等）——选题面向海外信息差
- ❌ 付费墙严重且无法获取摘要的源
- ❌ 质量参差不齐的自媒体/营销号
