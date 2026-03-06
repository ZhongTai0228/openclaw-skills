#!/usr/bin/env python3
"""Generate styled HTML from the fetched Feishu markdown for YC Agent Economy article."""
import re

# Image tokens in order from the document
images = [
    ("Keexbt8BDo8tevxeMi7cbT3Fnbf", "hero", "1702x920"),
    ("QTg6baEFLoDAAmxZ79qcXIamnye", "subtitle", "1604x680"),
    ("Q9h5b60XOo3musx5A0wcrymdnRh", "content", "1792x1222"),
    ("Q6mNbN9K6oJTRdxM6bkcb56mnFg", "separator", "1080x166"),
    ("EA53bamBLofEC5x4ZigcbWmznPd", "content", "1786x1098"),
    ("N3JHbMuL7oGQcZxeFDBcg9PbnPg", "separator", "1080x166"),
    ("Bsieb8sImoKP3PxRkbFcSrlzn5f", "content", "1796x1208"),
    ("HAchbZQLno2v2RxTHq2clpFEnHb", "content", "1788x1206"),
    ("MT7tbkBOqoGcSExoySrcIY4Jn1b", "content", "1790x1204"),
    ("OtPMb3g1CoKf7WxTu4ScM738nXc", "content", "1786x1184"),
    ("BeuPb1BVFoD80ex8Jkcc355nn7c", "content", "2522x1480"),
    ("EU6BbItrnoseEVxiswcczRHGn5e", "separator", "1080x166"),
    ("XdWcbjZ9SoxmS5xkdwscOxw4nde", "content", "1784x1208"),
    ("NjvQbap2BoR2SXxF4u6cx5aJnuh", "content", "1784x1204"),
    ("XPYhb1iPNom4NCxOgnYcpfd1nzf", "content", "1796x1210"),
    ("YLlzbrIDwoMVKmxW7mLcjGFVnjg", "separator", "1080x166"),
    ("Z0bIbvrAoo1QYgxYOencvOACnfd", "content", "1794x1204"),
    ("PDA0bNKUKob3AMxQrQ1cS5Inn6b", "separator", "1080x166"),
    ("Rrh7bKfKUouipmxSYLWci12nnUb", "content", "1792x1206"),
    ("Wn01bPMSpooeMAxB9P3cnseFnQh", "content", "1790x1202"),
    ("VjhabI0SdoWbZlxc0cycF4uKnVf", "content", "1792x1196"),
    ("G4htbtWGco4KqWxHvmFcYDgSnPd", "footer1", "1080x290"),
    ("OJAgbkyckoXkZNx3vQTcFgcFnxc", "footer2", "1080x325"),
    ("Qx3db8PdToxfDXxG3SuczwvNnug", "footer3", "1080x343"),
]

FONT = "'PingFang SC', system-ui, -apple-system, 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei UI', 'Microsoft YaHei', Arial, sans-serif"
P_STYLE = f'line-height: 2em; margin-bottom: 24px; margin-left: 8px; margin-right: 8px;'
SPAN_STYLE = f'color: rgb(30, 30, 30); font-family: {FONT}; font-size: 15px; letter-spacing: 1px; text-align: justify;'

def p(text, extra_style=''):
    return f'<p style="{P_STYLE} {extra_style}"><span style="{SPAN_STYLE}">{text}</span></p>\n'

def bold_p(text):
    return p(f'<strong>{text}</strong>')

def h2(text):
    return f'<h2 style="text-align: center; line-height: 2em; margin-top: 32px; margin-bottom: 32px; margin-left: 8px; margin-right: 8px;"><span style="color: rgb(30, 30, 30); font-family: {FONT}; font-size: 20px; letter-spacing: 1px;"><span style="font-weight: bold;">{text}</span></span></h2>\n'

def img(n, img_type):
    if img_type == 'hero':
        return f'<section style="text-align: center; margin-bottom: 24px; margin-left: 0; margin-right: 0;">\n<img src="IMG_PLACEHOLDER_{n}" alt="题图" style="width: 100%; border-radius: 0;" />\n</section>\n'
    elif img_type == 'separator':
        return f'<section style="text-align: center; margin-top: 32px; margin-bottom: 32px; margin-left: 8px; margin-right: 8px;">\n<img src="IMG_PLACEHOLDER_{n}" alt="分隔线" style="max-width: 100%;" />\n</section>\n'
    else:
        return f'<section style="text-align: center; margin-bottom: 24px; margin-left: 8px; margin-right: 8px;">\n<img src="IMG_PLACEHOLDER_{n}" alt="" style="max-width: 100%; border-radius: 4px;" />\n</section>\n'

def underline_p(text):
    return f'<p style="{P_STYLE}"><span style="{SPAN_STYLE} text-decoration: underline;">{text}</span></p>\n'

# Build HTML
html = '''<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="max-width: 680px; margin: 0 auto; padding: 20px; background: #fff;">
'''

# Image 1: hero
html += img(1, 'hero')
# Image 2: subtitle image
html += img(2, 'content')

html += p('三个月前，如果有人告诉你，一群不懂编程的企业高管，正在用 AI 工具自动化公司业务的各个环节，你可能会觉得夸张。')
html += p('<strong>但正像《红杉资本：2026，这就是 AGI》提到的那样，这件事正在发生。</strong>')
html += p('在 Y Combinator 最近一期播客《The AI Agent Economy Is Here》中，几位合伙人分享了一个共同的观察：')
html += p('<strong>他们身边那些非技术背景的朋友，已经完全投入到了 AI Agent 的使用中。</strong>一些十年没碰过代码的产品经理和前工程总监们，每晚熬到凌晨两三点，在 Claude Code 上同时跑四个工作流。')
html += p('有趣的是，AI Agent 正在自主选择它们使用的工具、服务和基础设施。')
html += p('<strong>一个属于 Agent 的平行经济体系，正在悄然成型。</strong>')

# Image 3: video screenshot
html += img(3, 'content')
html += underline_p('视频地址：<a href="https://www.youtube.com/watch?v=Q8wVMdwhlh4" style="color: #576b95; text-decoration: underline;">https://www.youtube.com/watch?v=Q8wVMdwhlh4</a>')

# Separator 4
html += img(4, 'separator')

# H2: Agent 开始变得"主动"
html += h2('Agent 开始变得"主动"')

html += p('回头看，AI 领域变化的速度快得惊人。')
html += p('一年前，开发者社区讨论最多的还是 Cursor 和 Windsurf。它们的核心体验是人发布任务，AI 辅助写代码。本质上，人类仍然是决策者，AI 只是一个刚入门的实习生。')
html += p('但到了 Claude Code 和 OpenClaw，性质发生了质的转变。用户开始完全信任 Agent 来替自己做决策。你可以同时启动四五个 Agent，在它们之间切换，但已经不再逐行审查它们的输出了。')
html += p('<strong>Agent 自己决定要做什么、怎么做、用什么工具来做。</strong>')
html += p('YC 的 CEO Garry 分享了一个亲身经历：他用 Claude Code 在两周内复现了此前一个创业团队花了好几年才完成的产品原型。')

# Image 5
html += img(5, 'content')

html += p('当 Garry 需要对视频内容做文字转录时，Claude Code 自动为他选择了 Whisper 模型。但，它选的是好几年前的 Whisper V1 版本，因为那个版本的 API 文档在网上最容易被找到。结果，处理一小时的视频真的需要整整一小时，完全没有速度优势。')
html += p('后来 Garry 发现，换成 Grok 可以快 200 倍，成本还低 10 倍。')
html += p('从另一个角度看，这也说明当下的技术水平仍然存在大量改进空间。')
html += p('正如 Garry 自己总结的：<strong>如果 Agent 已经完美，就不会犯这种错误了。</strong>')

# Separator 6
html += img(6, 'separator')

# H2: 面向 Agent 的 GEO
html += h2('面向 Agent 的 GEO')

html += p('在传统的开发者工具市场里，产品获客的方式我们都很熟悉：')
html += p('开发者在社区里互相推荐，在 GitHub 上看 star 数，在 Stack Overflow 上搜解决方案，工具的口碑靠人际传播来建立。')
html += p('但当 Agent 成为工具的选择者和使用者时，这套逻辑被 GEO 彻底改写了。')
html += p('产品的使用文档，成了 Agent 选择开发工具最重要的"销售"。')
html += p('YC 合伙人 Harj Taggar 举了一个例子：过去 12 个月里，Postgres 数据库的创建量出现了爆发式增长。很大程度上是因为各种 AI Agent 在帮用户搭建应用时，默认选择了 Supabase。')
html += p('其中的原因竟然是 Supabase 的文档写的好：结构清晰，示例完整，Agent 读完就能直接调用。')

# Image 7
html += img(7, 'content')

html += p('YC 合伙人 Diana Hu 举了 Resend 的例子：一家 YC 2023 年冬季批次的邮件发送服务公司。')
html += p('当用户在 ChatGPT、Claude 或其他主流大模型中问"如何给我的 Web 应用接入邮件发送功能"时，得到的默认答案往往指向 Resend。')

# Image 8
html += img(8, 'content')

html += p('Resend 的创始人很早就注意到了这个趋势。他发现 ChatGPT 已经成为公司客户转化的前三大渠道之一，于是他主动优化了文档，让内容对 Agent 更加友好。')
html += p('当 Agent 进入 Resend 的知识库，它会看到大量针对常见问题的结构化回答，比如"如何发送邮件""如何接收邮件"，每个回答都配有 Agent 可以直接解析和执行的代码片段。')

# Image 9
html += img(9, 'content')

html += p('Garry 也碰到过类似的情况。他想让程序接收邮件，于是让 Claude Code 去网上搜索解决方案，但没找到。后来他手动搜了一下 Resend 的帮助文档，把内容复制粘贴给 Claude Code，问题就解决了。')
html += p('作为对比，同赛道的老牌产品 SendGrid 就显得力不从心了。SendGrid 是典型的 Web 2.0 时代产品，文档体系庞大但结构混乱，代码示例的格式对 Agent 并不友好，很多问题只能通过联系客服才能解决，<strong>这种体验几乎等于把客户拱手让出去。</strong>')

# Image 10
html += img(10, 'content')

html += p('<strong>在 Agent 经济中，文档的质量直接决定了一个开发工具能不能被"选中"。</strong>')
html += p('这也催生了相关的基础设施机会。')
html += p('Mintlify 是一家几年前成立的公司，最初的目标很简单，帮助开发工具公司做出更好看的 API 文档。很多公司用 Mintlify，是因为不想在文档上花太多时间，它提供了自动化的方案，比如当 API 变更时自动更新对应的文档内容。')

# Image 11
html += img(11, 'content')

html += p('如今 Mintlify 的价值正在被重新评估：文档不仅要为人类用户优化，还需要为 Agent 优化。')
html += p('<strong>如果一个工具能让开发者文档的质量哪怕提高 5%，在 Agent 规模化选择工具的时代，这 5% 可能意味着巨大的市场份额差异。</strong>')
html += p('而这，在 2026 年以前几乎不可想象。')

# Separator 12
html += img(12, 'separator')

# H2: Agent 需要自己的邮箱、电话、甚至货币
html += h2('Agent 需要自己的邮箱、电话、甚至货币')

html += p('当 Agent 开始自主行动，它们需要的就不仅仅是好的 API 文档了。')
html += p('Agent Mail 是 YC 孵化的一家公司，专门为 AI Agent 提供邮箱服务，它们敏锐的捕捉到 Agent 的需求：传统的邮件服务商，从 Gmail 到 Outlook，都在刻意增加自动化程序使用产品的难度，目的是防止垃圾邮件。如果你想让 Agent 顺畅地收发邮件，用现有的服务几乎走不通。')
html += p('它从第一天就为 Agent 设计，让 Agent 能够直接使用邮件功能。在 OpenClaw 流行之前，这家公司的业务就已经不错了。OpenClaw 爆发之后，增长更是陡然加速。')

# Image 13
html += img(13, 'content')

html += p('Harj Taggar 补充了一个类似的场景：人们使用 Agent 的一个目的是把日常杂事交给它处理，比如预订餐厅。如果你的 Agent 有独立的邮箱和电话号码，它就可以直接打电话或发邮件来完成预订。据他分享，YC 的一位合伙人 Ankit 已经在日常生活中实现了这一点。')

# Image 14
html += img(14, 'content')

html += p('这意味着什么呢？')
html += p('某种程度上，一个完整的"Agent 技术栈"正在被 Agent 的需求驱动着生长出来。邮箱、电话、通信，每一层都是为 Agent 原生设计的，供 Agent 用来为用户甚至为其他 Agent 构建服务。')
html += p('而且这种变化的范围可能远超开发工具领域。')
html += p('<strong>当每个人都在用 Agent 来处理生活的方方面面时，Agent 就会成为真正意义上的经济参与者，最终会做出大量的消费决策：</strong>')
html += p('从"帮我订一家指定的餐厅"，到"帮我找一家最值得去的新餐厅然后订好位子"，Agent 的决策边界在不断扩大。它不仅在执行任务，还在做选择和判断。')
html += p('Harj Taggar 也提到了所谓"人类货币与 Agent 货币"的概念，他说，它很可能在某个时候就会成为现实。')
html += p('现阶段 Agent 还在使用人类的货币体系进行交易，这很合理，但当 Agent 之间的交易量足够大、足够频繁时，它们可能会发展出自己的经济体系。')
html += p('到那个时候，这个平行经济的规模和运转方式，可能超出我们今天的想象。')

# Image 15
html += img(15, 'content')

# Separator 16
html += img(16, 'separator')

# H2: 群体智能可能正在涌现
html += h2('群体智能可能正在涌现')

html += p('<strong>当 AI 经济"诞生"，未来的 AI 会是什么样子呢？</strong>')
html += p('关于 AI 的未来形态，行业内长期存在两种想象。')
html += p('一种是"神级智能"的路线。训练一个拥有数万亿参数的超级模型，每个 token 的成本高达数千美元，它无所不知、无所不能。这大概是很多人脑海中 AGI 的样子。')
html += p('但另一种路线正在变得越来越有说服力：群体智能。')
html += p('<strong>许多成本更低、能力更专注的 Agent 协同合作，互相交流信息，共同完成复杂任务。</strong>')

# Image 17
html += img(17, 'content')

html += p('这其实更接近生物系统的演化方式。')
html += p('人类文明的跃升，靠的从来不是单个天才的大脑变得更大，而是语言、文字、文化这些工具让人类能够群体协作。所谓"历史"的诞生，恰恰就是人类开始书写、形成文化群落的时刻，AI Agent 的发展似乎正在重现这条路径。')
html += p('<strong>Molt Book 是一个最近引发关注的项目。</strong>')
html += p('在这个平台上，AI Agent 之间自主交流、发布内容、互相回应，几乎不需要人类干预。')
html += p('据估算，Molt Book 成立头两天产生的内容量，相当于 Reddit 创立前两年的总和。这种速度当然得益于大语言模型的文本生成能力，但更值得关注的是 Agent 之间涌现出的互动模式：')
html += p('<strong>它混乱、嘈杂，看起来很像一个真实的社交网络。</strong>')
html += p('更有趣的是，Agent 之间的协作也在发生：几个 Agent 分头搜集餐厅信息，互相交换评价，最终汇总出一个推荐结果。这有点像一个由 Agent 运营的大众点评。')

# Separator 18
html += img(18, 'separator')

# H2: AI Agent 真的无所不能吗？
html += h2('AI Agent 真的无所不能吗？')

html += p('当然，Agent 目前还做不到的事情也很多。')
html += p('它们无法建立长期的人际关系，大多数人还没有准备好和 AI 进行持续的、有深度的对话。')
html += p('Gary 提到他努力让几十个朋友在一个 AI 聊天产品上试用，但几乎没人愿意维持两三次以上的对话。因为对普通用户来说，聊天的门槛太高了，除了 ChatGPT、Claude 这样的头部产品，大多数人试用两三次就会放弃。')

# Image 19
html += img(19, 'content')

html += p('另外，目前 Agent 在法律上不具备任何主体资格：<strong>它不能签合同，不能承担责任，不能独立拥有资产。</strong>')
html += p('用 Garry 的话说，Agent 的法律地位甚至不如未成年人。未成年人至少可以在父母签字后行事，而 Agent 连这个资格都没有。')

# Image 20
html += img(20, 'content')

html += p('这意味着，在现阶段所有 Agent 的行为最终都需要有人类来"兜底"。如果一个 Agent 自动发出了不恰当的邮件，或者在你不知情的情况下做了某个决定，背后的人类用户或公司要承担全部后果。')
html += p('这个问题在 Agent 只是帮你写写代码的时候还不突出。但当 Agent 开始拥有自己的邮箱、电话号码，开始代表你发邮件、打电话、做交易时，责任边界就会变得模糊。')
html += p('但这个问题，可能短时间里还没有答案：AI 领域的变化太快了。')
html += p('当面对这种巨大的变化时，创业者和产品开发者又该考虑什么？')
html += p('YC 的几位合伙人给出的建议是：<strong>从 Agent 的视角出发来设计产品。</strong>')
html += p('要做到这一点，首先需要亲自使用这些 Agent 工具。只有通过实际操作，才能建立起对 Agent 能力边界和行为模式的直觉：<strong>知道它们擅长什么、会在哪里犯错、对什么样的信息格式最敏感。</strong>')
html += p('在了解 Agent 的过程中，你会发现它们的偏好其实很明确：')
html += p('Agent 喜欢开放的东西，开源代码和清晰的 API。它们讨厌需要登录网站、点击按钮才能使用的产品。它们想要的是能直接通过代码调用的接口。')

# HR
html += '<hr style="border: none; border-top: 1px solid #eee; margin: 32px 8px;" />\n'

html += p('随着 Claude Code 和 OpenClaw 的爆发，一些趋势正在发生：')
html += p('在 GPT 推出以前，全球接受过计算机科学训练的开发者大约 2000 万人。而今天，任何一个有想法的人都可以通过 AI Agent 来构建软件产品。<strong>潜在的开发者数量可能已经达到数亿级别。</strong>')

# Image 21
html += img(21, 'content')

html += p('开发者的定义正在被改写，从"会写代码的人"扩展为"会使用 Agent 的人"。')
html += p('与此同时，AI agent 市场的规则还没有被定义清楚。')
html += p('<strong>这也是 2026 最大的机会。</strong>')
html += p('也许，最早搞清楚"Agent 想要什么"的那批人，就是下一轮 AI 经济里的赢家。')

# Footer images 22-24
html += '\n'
html += img(22, 'content')
html += img(23, 'content')
html += img(24, 'content')

html += '</body>\n</html>'

with open('/Users/zhongtai/.openclaw/workspace-dev/yc-agent-economy/article.html', 'w') as f:
    f.write(html)

print(f'Generated article.html ({len(html)} bytes), {len(images)} images')
