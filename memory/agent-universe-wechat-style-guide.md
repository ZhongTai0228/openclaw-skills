# 公众号排版风格指南（观猹笔记）

参考文章：https://mp.weixin.qq.com/s/euhfumz7XUtbI2S2FgmZwA
"复盘 AI 陪伴消亡史：我们究竟做错了什么？"

## 正文段落
- `line-height: 2em`
- `margin-bottom: 24px`
- `margin-left: 8px; margin-right: 8px`
- 字体：`"PingFang SC", system-ui, -apple-system, system-ui, "Helvetica Neue", "Hiragino Sans GB", "Microsoft YaHei UI", "Microsoft YaHei", Arial, sans-serif`
- 字号：`15px`
- 颜色：`rgb(30, 30, 30)`
- 字距：`letter-spacing: 1px`
- 对齐：`text-align: justify`（所有非 H2 内容均两端对齐）

## H2 标题
- **居中对齐**（`text-align: center`）
- `margin-top: 32px; margin-bottom: 32px`
- `margin-left: 8px; margin-right: 8px`
- 内部 span：`font-size: 20px; font-weight: bold; letter-spacing: 1px`
- 颜色同正文 `rgb(30, 30, 30)`
- 仅用于真正的章节标题（如"一只 OpenClaw 的 Book 日记""我所知道的""我不知道的事"）
- **日期标题（1 月 30 日等）不是 H2**，而是加粗的两端对齐段落（`font-size: 17px`）

## 引号规范
- **必须使用中文弯引号** `""` `''`
- **禁止使用**：英文直引号 `""`、日式引号 `「」`、全角引号 `＂＂`
- 所有引用内容、术语引用、对话引用一律用 `""` 包裹

## 中英文间距规范
- 中文与英文/数字之间加一个空格（如 `Claude 宪章`、`150 万`）
- **英文前后如果紧跟中文标点，不加空格**（如 `"OpenClaw 塌房了"` 而非 `"OpenClaw 塌房了 "`）
- 中文标点包括：，。！？：；、""''（）《》【】…—

## 题图（第一张图）
- **通栏显示，无左右间距**（`margin-left: 0; margin-right: 0; width: 100%; border-radius: 0;`）
- 其他普通图片保持 `margin-left: 8px; margin-right: 8px; max-width: 100%; border-radius: 4px;`

## 图片说明文字
- 用 `<span>` 包裹，`color: rgb(136, 136, 136)`（灰色）
- 字号：`12px`
- 通常在图片下方

## 分隔图片
- 居中，`text-align: center`
- `margin-top: 32px; margin-bottom: 32px`

## 列表
- 使用悬挂缩进：`text-indent: -0.8em; padding-left: 0.8em`
- 两端对齐（`text-align: justify`）

## 脚注引用
- 用 `[1]` `[2]` 等形式
- `font-size: 12px` 或 `13px`

## 加粗
- 用 `<strong>` 标签，无额外样式
- 使用克制，用于总结性金句或关键信息

## 封面与摘要
- 封面从正文选择，需认真裁剪 2.35:1 和 1:1 两种比例
- 摘要 15 字以内，吸引人，末尾需有标点符号

## 总体特点
- **简洁克制**：没有花哨装饰、没有彩色背景块、没有 blockquote 装饰
- **行间距宽松**：2em 行高 + 24px 段间距，阅读舒适
- **左右留白**：8px margin（题图除外）
- **字距微调**：1px letter-spacing
- **深灰文字**：不用纯黑，用 rgb(30,30,30)
