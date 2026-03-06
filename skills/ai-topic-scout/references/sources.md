# AI Topic Scout - 信息源与扫描策略

## 信息源列表

### 1. X/Twitter AI KOL
通过 web_search 搜索近期推文：
- @sama (Sam Altman, OpenAI CEO)
- @kaboringAI (Karina Nguyen)
- @ylecun (Yann LeCun, Meta AI)
- @demaboringAI (Demis Hassabis, DeepMind)
- @AnthropicAI
- @ClementDelwordle (Clem Delangue, Hugging Face)
- @jimfan (Jim Fan, NVIDIA)
- @kaboringAI
- @emaboringollick (Ethan Mollick)

搜索查询示例：
- `site:x.com AI announcement today`
- `from:sama OR from:ylecun AI`

### 2. 官方博客
| 来源 | URL | 扫描策略 |
|---|---|---|
| OpenAI Blog | openai.com/blog | `site:openai.com/blog` |
| Anthropic Blog | anthropic.com/research | `site:anthropic.com` |
| Google DeepMind | deepmind.google/discover | `site:deepmind.google` |
| Meta AI Blog | ai.meta.com/blog | `site:ai.meta.com/blog` |
| Mistral Blog | mistral.ai/news | `site:mistral.ai/news` |

### 3. 科技媒体
| 来源 | 搜索查询 |
|---|---|
| TechCrunch | `site:techcrunch.com AI` |
| The Verge | `site:theverge.com AI` |
| Ars Technica | `site:arstechnica.com AI` |
| Wired | `site:wired.com artificial intelligence` |

### 4. 社区
| 来源 | URL / 查询 |
|---|---|
| Hacker News | `site:news.ycombinator.com AI` + web_fetch `https://hn.algolia.com/api/v1/search?query=AI&tags=story&hitsPerPage=10` |
| Reddit r/MachineLearning | `site:reddit.com/r/MachineLearning` |

### 5. 播客
| 播客 | 搜索查询 |
|---|---|
| Latent Space | `site:latent.space` |
| Lex Fridman | `site:lexfridman.com` OR `Lex Fridman podcast AI` |
| The AI Podcast (NVIDIA) | `NVIDIA AI podcast latest episode` |
| Cognitive Revolution | `cognitive revolution podcast AI latest` |
| Last Week in AI | `last week in AI podcast latest` |

## 扫描策略

### 搜索查询组合（每轮执行）
每轮扫描执行以下 web_search 查询（freshness="pd" 限定 24 小时内）：

1. **综合热点**: `AI breakthrough OR AI launch OR AI release today 2026`
2. **模型发布**: `new AI model release GPT Claude Gemini Llama`
3. **产品动态**: `AI product launch startup funding 2026`
4. **开源动态**: `open source AI model release huggingface`
5. **政策法规**: `AI regulation policy government`
6. **Agent/应用**: `AI agent autonomous tool use`
7. **行业影响**: `AI impact industry enterprise adoption`

### 去重策略
- 用选题标题关键词在多维表格中搜索，避免重复选题
- 相似新闻合并为一个选题，多个信息源作为参考

### 选题提炼原则
1. **不是新闻搬运**：不要"OpenAI 发布了 X"，而要"X 意味着什么？对 Y 有何影响？"
2. **有角度**：每个选题必须有明确的切入点
3. **有读者价值**：说明为什么特工宇宙的读者会关心
4. **时效性判断**：区分"必须今天写"和"可以慢慢写"
