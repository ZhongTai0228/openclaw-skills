# 风格模板：摸鱼小李

> 来源：https://mp.weixin.qq.com/s/vbfc9EQmWq0XqRrkW_JJgw
> 提取时间：2026-03-07
> 公众号：摸鱼小李

---

## 整体设计

- **最大宽度**: 677px
- **背景色**: #FFFFFF
- **主色调**: `#059669`（绿色，翡翠绿）
- **辅助绿**: `#10B981`、`#34D399`、`#A7F3D0`、`#ECFDF5`
- **文字色系**: `#111827`（标题深黑）、`#374151`（正文深灰）、`#4B5563`（中灰）、`#9CA3AF`（浅灰辅助）、`#D1D5DB`（极浅灰）
- **字体**: `"PingFang SC", -apple-system, BlinkMacSystemFont, "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- **全局行高**: 1.75
- **全局字间距**: 0.5px

## 正文段落

```css
p {
  font-size: 14px;
  color: #4B5563;  /* 或 #374151 */
  line-height: 1.8 ~ 1.9;
  text-align: justify;
  margin-bottom: 20px;
  /* 左右 padding 在外层 section 控制：padding: 0 20px; */
}
```

## 标题系统

### 章节标题（H3 级）
采用独特的**大号编号 + 标题 + 副标题**三段式：

```html
<section style="display: flex; align-items: center; margin-bottom: 24px;">
  <!-- 大号空心编号 -->
  <span style="font-size: 36px; font-weight: 900; color: transparent; -webkit-text-stroke: 1.5px #D1D5DB; line-height: 1; margin-right: 14px;">01</span>
  <h3 style="font-size: 16px; font-weight: 800; color: #111827; margin: 0; letter-spacing: 0.5px;">
    主标题
    <span style="font-size: 13px; font-weight: 400; color: #9CA3AF; margin-left: 6px;">/ 副标题</span>
  </h3>
</section>
```

**特点**：
- 编号用 `-webkit-text-stroke` 实现空心字效果
- 编号 36px 超大号，颜色透明+描边 `#D1D5DB`
- 主标题 16px，font-weight 800
- 副标题 13px，`#9CA3AF`，用 `/` 分隔
- 章节间距: `margin-top: 48px; margin-bottom: 32px;`

## 高亮样式

### 1. 渐变高亮（最常用，用于重点句子）
```css
span {
  background: linear-gradient(120deg, #FDE68A 0%, rgba(255,255,255,0) 100%);
  padding: 0 4px;
  border-radius: 2px;
  font-weight: 600;
  color: #111827;
}
```
黄色渐变消退效果，非常有辨识度。

### 2. 代码/标签式高亮（用于术语）
```css
span {
  background: #F3F4F6;
  color: #1F2937;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 600;
}
```

### 3. 下划线高亮（用于关键短语）
```css
span {
  border-bottom: 2px solid #A7F3D0;
  font-weight: 600;
}
```
绿色下划线，配合 bold。

### 4. 品牌名/产品名高亮
```css
strong {
  color: #059669;
}
```
直接用主色调加粗。

## 图片样式

### 内容图片（卡片式）
```html
<section style="background: #FFF; border-radius: 12px; padding: 6px; border: 1px solid #F3F4F6; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 24px;">
  <figure style="margin: 0; border-radius: 8px; overflow: hidden;">
    <img style="width: 100%; display: block;" />
  </figure>
</section>
```
- 图片有白色卡片边框 + 轻微阴影
- 外层 12px 圆角，内层 8px 圆角
- 6px padding 形成白色边框效果
- 边框: `1px solid #F3F4F6`

### 头图
```css
img {
  border-radius: 18px;
  background-color: transparent;
  width: 100%;
}
```
- 较大的 18px 圆角
- 全宽

### 尾图
```css
img {
  border-radius: 15px;
  background-color: transparent;
  width: 100%;
}
```

## 特殊组件

### Hero 卡片（文章开头大卡片）
```css
section {
  margin: 0 0 32px;
  background: #FFF;
  border: 1.5px solid rgba(5, 150, 105, 0.15);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}
```
- 带绿色半透明边框
- 20px 大圆角
- 内部有装饰元素：小绿圆点 + 标签 + 渐变分隔线
- 底部绿色渐变条: `background: linear-gradient(135deg, #059669, #10B981)`

### 标签栏（Hero 卡片底部）
```html
<section style="background: linear-gradient(135deg, #059669, #10B981); padding: 12px 28px; display: flex; align-items: center; justify-content: space-between;">
  <p style="font-size: 12px; color: rgba(255,255,255,0.9); font-weight: 600;">左侧文字</p>
  <section style="display: flex; gap: 4px;">
    <span style="background: rgba(255,255,255,0.2); padding: 1px 6px; border-radius: 3px; font-size: 8px; color: #fff; font-weight: 600;">标签</span>
  </section>
</section>
```

### KEY INSIGHT 引用块
```html
<section style="margin-bottom: 24px;">
  <!-- 标签 -->
  <section style="display: inline-block; background: #059669; color: #fff; padding: 4px 14px; border-radius: 6px 6px 0 0; font-size: 10px; font-weight: 700; letter-spacing: 1px;">
    KEY INSIGHT
  </section>
  <!-- 内容 -->
  <section style="background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 0 12px 12px 12px; padding: 20px 24px;">
    <p style="font-size: 14px; color: #374151; margin: 0; line-height: 1.8; font-style: italic;">
      引用内容
    </p>
  </section>
</section>
```
- 上方绿色标签，左上角方角（与内容连接），右上角圆角
- 内容区域浅灰背景，斜体

### 痛点列表
```html
<section style="display: flex; align-items: flex-start; gap: 10px; margin-bottom: 14px;">
  <span style="background: #1F2937; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 700; flex-shrink: 0;">痛点 1</span>
  <p style="font-size: 14px; color: #374151; margin: 0; line-height: 1.6;">描述文字</p>
</section>
```
- 深色标签 `#1F2937`
- flex 布局，标签不换行

### 期待列表（绿色标签版）
```html
<section style="display: flex; align-items: flex-start; gap: 8px; margin-bottom: 16px;">
  <span style="background: #059669; color: #fff; padding: 1px 5px; border-radius: 3px; font-size: 9px; font-weight: 700; flex-shrink: 0; margin-top: 3px;">期待 1</span>
  <p style="font-size: 14px; color: #374151; margin: 0; line-height: 1.8;">描述文字</p>
</section>
```

### 视频卡片
```html
<section style="background: #fff; border-radius: 16px; padding: 12px; margin-bottom: 32px; border: 2px solid #059669; box-shadow: 0 4px 12px rgba(5,150,105,0.1);">
  <!-- 标签行 -->
  <section style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
    <span style="width: 8px; height: 8px; background: #059669; border-radius: 50%;"></span>
    <span style="font-size: 11px; color: #059669; font-weight: 700; letter-spacing: 1px;">VIDEO 01</span>
    <span style="flex: 1; height: 1px; background: linear-gradient(to right, rgba(5,150,105,0.2), transparent);"></span>
  </section>
  <!-- 视频嵌入区域 -->
</section>
```

### 横向滑动卡片组（目录导航）
```html
<section style="overflow-x: scroll; -webkit-overflow-scrolling: touch; white-space: nowrap; padding-bottom: 8px;">
  <!-- 第一张卡片（主色调） -->
  <section style="display: inline-block; white-space: normal; vertical-align: top; width: 110px; background: linear-gradient(135deg, #059669, #10B981); border-radius: 12px; padding: 12px; margin-right: 8px;">
    <p style="font-size: 9px; font-weight: 700; color: rgba(255,255,255,0.7); letter-spacing: 1px; margin: 0 0 5px;">PART 01</p>
    <p style="font-size: 13px; font-weight: 800; color: #fff; margin: 0 0 3px;">标题</p>
    <p style="font-size: 10px; color: rgba(255,255,255,0.7); margin: 0;">副标题</p>
  </section>
  <!-- 后续卡片（白色） -->
  <section style="display: inline-block; white-space: normal; vertical-align: top; width: 110px; background: #fff; border: 1px solid #E5E7EB; border-radius: 12px; padding: 12px; margin-right: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
    ...
  </section>
</section>
```

### 尾部互动区
```html
<section style="background: radial-gradient(circle at center, #F9FAFB 0%, #FFFFFF 100%); border: 1px solid #E5E7EB; border-radius: 16px; padding: 32px 20px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
  <p style="font-size: 13px; font-weight: bold; color: #111827; margin: 0 0 20px; line-height: 1.6;">
    互动提问
  </p>
  <!-- 点赞/在看/分享 图标行 -->
  <p style="font-size: 10px; color: #9CA3AF; letter-spacing: 1px; margin: 0;">THANKS FOR READING</p>
</section>
```

## 装饰元素

### 小绿圆点
```css
span { width: 6px; height: 6px; background: #059669; border-radius: 50%; }
```

### 渐变分隔线
```css
span { flex: 1; height: 1px; background: linear-gradient(to right, rgba(5,150,105,0.12), transparent); }
```

### 短粗色条
```css
section { width: 48px; height: 3px; background: linear-gradient(to right, #059669, #34D399); border-radius: 2px; }
```

## 间距规律

- 正文段落间距: `margin-bottom: 20px`
- 图片卡片间距: `margin-bottom: 24px`
- 章节间距: `margin-top: 48px; margin-bottom: 32px`
- 内容区域 padding: `0 20px`
- Hero 卡片内 padding: `32px 28px 28px`

## 整体风格总结

1. **现代科技感**: 大量圆角、阴影、渐变
2. **绿色主题**: 翡翠绿为品牌色，贯穿全文
3. **卡片化设计**: 图片和特殊区块都用卡片包裹
4. **多层次排版**: 空心大号编号、多种高亮方式、标签化信息
5. **英文点缀**: "KEY INSIGHT"、"PART 01"、"SUMMARY" 等英文标签增加国际感
6. **渐变使用**: 绿色渐变条、黄色渐变高亮、分隔线渐变消退
