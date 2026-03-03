#!/usr/bin/env python3
# Generate styled HTML for WeChat 公众号

STYLE_SPAN = 'color: rgb(30,30,30); font-family: "PingFang SC",system-ui,-apple-system,"Helvetica Neue","Hiragino Sans GB","Microsoft YaHei UI","Microsoft YaHei",Arial,sans-serif; font-size: 15px; letter-spacing: 1px;'
STYLE_P = 'line-height: 2em; margin-bottom: 24px; margin-left: 8px; margin-right: 8px; text-align: justify;'
STYLE_H2 = 'text-align: center; line-height: 2em; margin-top: 32px; margin-bottom: 32px; margin-left: 8px; margin-right: 8px;'
STYLE_H2_SPAN = 'color: rgb(30,30,30); font-family: "PingFang SC",system-ui,-apple-system,"Helvetica Neue","Hiragino Sans GB","Microsoft YaHei UI","Microsoft YaHei",Arial,sans-serif; font-size: 20px; letter-spacing: 1px;'
STYLE_GRAY = 'color: rgb(140,140,140); font-family: "PingFang SC",system-ui,-apple-system,"Helvetica Neue","Hiragino Sans GB","Microsoft YaHei UI","Microsoft YaHei",Arial,sans-serif; font-size: 13px; letter-spacing: 1px;'

img_idx = [0]
def img(is_hero=False, is_sep=False):
    img_idx[0] += 1
    n = img_idx[0]
    if is_hero:
        return f'<section style="text-align: center; margin-bottom: 24px; margin-left: 0; margin-right: 0;"><img src="IMG_PLACEHOLDER_{n}" style="width: 100%; border-radius: 0;" /></section>'
    elif is_sep:
        return f'<section style="text-align: center; margin-top: 32px; margin-bottom: 32px; margin-left: 8px; margin-right: 8px;"><img src="IMG_PLACEHOLDER_{n}" style="max-width: 100%;" /></section>'
    else:
        return f'<section style="text-align: center; margin-bottom: 24px; margin-left: 8px; margin-right: 8px;"><img src="IMG_PLACEHOLDER_{n}" style="max-width: 100%; border-radius: 4px;" /></section>'

def p(text):
    return f'<p style="{STYLE_P}"><span style="{STYLE_SPAN}">{text}</span></p>'

def bold_p(text):
    return f'<p style="{STYLE_P}"><span style="{STYLE_SPAN}"><strong>{text}</strong></span></p>'

def gray_p(text):
    return f'<p style="{STYLE_P}"><span style="{STYLE_GRAY}">{text}</span></p>'

def h2(text):
    return f'<h2 style="{STYLE_H2}"><span style="{STYLE_H2_SPAN}"><span style="font-weight: bold;">{text}</span></span></h2>'

def hr():
    return '<hr style="border: none; border-top: 1px solid #eee; margin: 32px 8px;" />'

parts = []
parts.append('<html lang="zh-CN"><head><meta charset="UTF-8"></head>')
parts.append('<body style="max-width: 680px; margin: 0 auto; padding: 20px; background: #fff;">')

# Hero image
parts.append(img(is_hero=True))  # 1

parts.append(p('AI 竞赛的节奏快得惊人，但产品层面却逐渐陷入单调重复。'))
parts.append(p('每个新模型刚登场时都能碾压所有竞品，直到下一个更强的版本出现。'))
parts.append(p('大家都在做"各种素材整合"的文章：'))
parts.append(bold_p('无数 Agent 被投入使用，试图通过串联数据点创造价值，结果却常常帮倒忙。'))
parts.append(p('不过，从品牌建设的角度来看，AI 领域的品牌价值从未像今天这样引人关注。在产品同质化严重的红海市场里，品牌已成为企业争夺注意力、权威地位和资本的核心资产。'))
parts.append(bold_p('眼下，从品牌视角切入 AI 领域恰逢其时。'))
parts.append(bold_p('今天，请留出点时间，不要再思考枯燥的产品逻辑，请放下大脑，用心感受：'))
parts.append(bold_p('让我们一起欣赏关于 AI 产品背后的美学。'))

# Separator
parts.append(img(is_sep=True))  # 2

parts.append(p('关于 AI 的设计美学，我们的基础洞察是以下三点：'))
parts.append(bold_p('1、自然的亲和力，让本可能令人恐惧的技术，多了几分友好的吸引力。'))
parts.append(p('最直观的感受是，许多品牌都在追求一种自然舒适的氛围，给本可能让人畏惧的技术赋予亲和力。米白色系和柔和的自然渐变色调，传递出平静、亲和与可靠的气质。'))
parts.append(bold_p('2、当产品看上去大同小异时，富有表现力的关键视觉能帮它脱颖而出。'))
parts.append(p('除了这些简洁美观的界面底版外，不少品牌还会用富有表现力的核心视觉元素来打造差异化。在产品界面本身差异不大的领域，这种做法很合理。'))
parts.append(p('视觉风格的跨度很大：既有像素艺术、CAD 风格插画这类偏技术感的设计，突出技术本身；也有人物主题的绘画和随手涂鸦，强调技术能为人们带来什么。'))
parts.append(bold_p('3、AI 在人们心中的意象各不相同：有的是贴心助手，有的则意味着彻底颠覆。'))
parts.append(p('这些画面主题既有日常熟悉的场景，也有充满想象的未来构想。'))
parts.append(p('日常画面与亲切面孔传递出一个理念：AI 是来改善我们生活的工具；而复古未来主义的图像与神秘物件，则将 AI 塑造成即将彻底改变世界的技术。'))

parts.append(img())  # 3 content
parts.append(img(is_sep=True))  # 4 separator

parts.append(p('在 AI 的设计视觉趋势上，<strong>我们梳理出 14 个塑造 AI 视觉标识的关键趋势。</strong>'))
parts.append(p('而任何趋势都一样，盲目跟风只会导致千篇一律，最终被市场遗忘。'))
parts.append(p('真正的机会在于主动选择：<strong>何时跟进，何时观望，何时推波助澜，何时逆势而为</strong>'))

parts.append(img())  # 5

# Trend 1-14
trends = [
    ("1、近白色调", [
        'AI 的低调奢华设计范式：平静、温暖的柔和色调，旨在减少视觉干扰，规避设计风险。',
        '它传递的是信任、克制与成熟感，而非单纯的兴奋刺激。高端却不浮夸，权威而不强势。作为中性背景刻意退居幕后，让产品与内容叙事成为舞台焦点。',
        '2026 年的潘通年度色，早已在 AI 领域全面铺开。',
    ], '编者注：由潘通公司每年发布的、被广泛用于时尚、设计等领域的代表性色彩，用于反映当年的流行趋势与文化氛围。'),
    ("2、渐变设计", [
        '渐变设计简直无处不在：',
        '它们适配性强，百搭又不挑场景，无需过多修饰就自带吸引力。',
        '连 AI 都摸透了这个门道，在它设计的每个界面上都用上了渐变。',
        '为了脱颖而出，品牌们开始把渐变玩出新花样：让它更具有机感，加入颗粒、纹理和细微变化。',
        '最终，在同质化严重的拥挤市场里，这些品牌收获了更鲜明的辨识度和更独特的视觉标识。',
    ], None),
    ("3、数字印象派", [
        '数字印象派风格主要表现为柔和模糊的形态、简化的细节。',
        '这种表现方式刻意避开字面写实，转而聚焦于氛围营造和情感共鸣。画面里没有任何元素是完全清晰的，这种处理方式巧妙地避开了对 AI 本质或工作原理的生硬解释与过度定义。',
        '这种视觉语言不再是直白的描述，而是充满暗示性，给观众留出了想象和解读的空间。',
        '数字印象派（Digital impressionism）让品牌能够将"智能"可视化，同时避免做出那些自己无法完全掌控的具体承诺。',
    ], '编者注：Lom 风格影像是一种强调随意性、即时性的影像风格，常以充满生活气息的日常场景为创作对象，通过简约构图、自然光影及略带颗粒感或色彩失真的画面质感，传递出真实而富有个人情绪的瞬间表达。'),
    ("4、Lom 影像", [
        'lomography 风格的影像，把不完美当作一种标志。',
        '高对比度、褪色的色彩、漏光、模糊，还有那些肉眼可见的"小失误"，都是故意用来对抗精致的企业美学的。这种视觉语言把 AI 塑造成探索者，而非权威：是可以把玩的对象，不是让人望而生畏的存在。',
        '通过借鉴胶片摄影和那些"意外之喜"，这些品牌把自己和人类的创造力、好奇心、实验精神拉得更近。这种"杂乱感"是刻意为之的：它传递出开放、探索的意味，暗示这是一个仍在进化的系统，而非已经定型的僵化产品。',
    ], '编者注：一种以独特的视觉风格著称，常通过夸张的色彩、轻微的颗粒感、随性的构图以及充满生活气息的记录方式展现光影魅力，注重捕捉瞬间情绪与真实生活片段的影像创作风格。'),
    ("5、当代现实主义", [
        '当代现实主义既是 AI 的绝佳隐喻，也直观证明了它的能力。',
        '它能将无形化为有形，把原本模糊抽象的技术稳稳锚定在现实世界里。这种风格传递出精准、可控和匠心的特质，给人一种可靠且专业的感觉。',
        '它让品牌跳出模糊的装饰性渐变风格，同时暗示 AI 有一种不可思议的能力：能"看见"并解读世界。这就把技术定位成了既先进又易懂的存在。',
    ], '编者注：一种关注当代社会现实、强调写实性表达的艺术流派'),
    ("6、草图与涂鸦", [
        '草图与涂鸦，是对机器完美主义的刻意反叛。',
        '歪歪扭扭的线条、仓促的标记、未完成的草图，这些不是最终的成果，而是思考过程留下的视觉印记。',
        '它们让人联想到笔记本上的随手记录、白板上的临时草稿，以及那些想法尚在萌芽、还未定型的早期瞬间。在这个被自动化和规模化主导的世界里，这些随性的痕迹重新带回了犹豫、好奇和人类的真实意图。',
        '这种风格传达的是探索而非定论，它突出了技术背后的人类思考过程。',
    ], None),
    ("7、非品牌学术风", [
        '在这个看似遍地"突破性 AI"、实则大多不过是 GPT 包装的领域里，我们要建立真正的权威。',
        '视觉识别被精简到本质：拒绝花哨设计，抛弃以噱头为目的的营销。创新无需刻意彰显，作品本身就是最好的证明。简洁的排版、柔和的色彩、实用的布局，处处透出专业与可信。',
        '这是品牌的低调告白：我们不需要花里胡哨的外衣，实力自会发声。整体呈现出一种沉稳自信、严谨专业且充满权威感的气质。',
    ], None),
    ("8、技术插画", [
        '这个风格，通常并非技术本身的可视化呈现，而是技术实力的信号。',
        '与其说是沟通工具，不如说是装饰元素，借鉴了工程设计、研究论文和系统框图的风格。',
        '风格略带复古感，传递出严谨、深度与专业的气质。这种风格借鉴了技术文档的表达语言，将品牌塑造成知识渊博、精准且扎根于技术专长的形象。',
    ], None),
    ("9、古灵精怪的可爱", [
        '可爱的吉祥物，是对抗 AI 末日论的温柔平衡。',
        '它们把抽象、强大又有时带威胁感的技术变得有温度，让复杂系统有了友好的面孔。',
        '俏皮中带着 geek 气质，还自带点自嘲的幽默感，既是连接工程文化与圈内梗的桥梁，也能在公众面前传递亲和力，在 AI 人才争夺战中帮助团队营造归属感。',
    ], None),
    ("10、非凡物件", [
        '流动不息，演化不止，始终处于动态之中。没有固定形态，没有终极状态。形态在不断演化、消散又重组。呈现的是涌现过程，而非最终结果。',
        '这恰是那些持续学习、适应、随时间演化的系统的隐喻。它传递着新颖、未知与不确定性。AI 不是一件完工的产品，而是一个不断生成的过程。',
    ], None),
    ("11、未来主义超现实", [
        '有些品牌会打造一整个超现实的世界：',
        '层层叠叠的场景、打破常规物理法则的设定、如梦似幻的装置。时而带有蒸汽朋克风格，时而偏向复古未来主义，但始终充满异世界感。',
        '它们不怎么解释技术本身，更关注技术能带来什么可能。',
        '这传递出一个信号：这款 AI 不只是工具，更是一扇门，邀请你踏入全新的世界。',
    ], '编者注：一种起源于 20 世纪初，融合未来主义对速度、科技的推崇与超现实主义对潜意识、梦境意象的探索，常以夸张变形、荒诞组合、强烈视觉冲击为特征，追求突破现实逻辑以展现非理性精神世界的艺术流派。'),
    ("12、外太空", [
        '"终极边界"',
        '这个形容智能的比喻虽已为人熟知，但智能本身却依然像一片未被完全探索的领域。有时它浪漫而乌托邦，有时又难免显得老套。',
        '星系、恒星、宇宙之光：AI 就像一场探索，把每一步进展都看作是向未知领域的旅程。',
    ], None),
    ("13、ASCII 编码与像素", [
        '像素艺术和 ASCII 艺术卷土重来了。',
        '这是对早期互联网与电脑文化的致敬：设计自带复古感，一看就很亲切。',
        '这种 AI 不是来抢你饭碗的，而是用来玩的：既有创意又能启发灵感，同时还带着明确的技术感。它给本来看起来高深莫测的技术，增添了熟悉感、怀旧情绪和可预测性。',
    ], None),
    ("14、生成艺术", [
        '算法生成的图案、元胞自动机、基于规则的视觉效果：这些是艺术家和数学家常用的创作工具。',
        '它们是通过逻辑生成形态的系统，灵活且可扩展，与 AI 品牌的调性天生契合：视觉本身就像产品一样运作，重点不在于单一图像，而在于一个"活"的系统。',
        '这种视觉语言传递出深度、严谨性和涌现式复杂的信号。',
    ], None),
]

for title, paragraphs, editor_note in trends:
    parts.append(h2(title))
    if editor_note:
        parts.append(gray_p(editor_note))
    for text in paragraphs:
        parts.append(p(text))
    parts.append(img())  # each trend has one image after

# Separator before archetypes
parts.append(img(is_sep=True))  # 20

parts.append(p('我们分析过的每个品牌都各有特色，但它们可以归为五类鲜明的品牌原型：'))
parts.append(bold_p('每类在争夺注意力、话语权与资本的角逐中，都展现出独特的风格。'))
parts.append(gray_p('编者注：品牌原型，即品牌人格化的经典模型，用于定义品牌的核心特质与情感定位'))

parts.append(img())  # 21

archetypes = [
    ("1、亲和型领袖", [
        'OpenAI、Sierra、Cursor 这类品牌主打严肃、稳定与信任感。',
        '它们的色调都很低调，常用柔和的灰色与温暖的米色打底：没有刺眼的亮色，也没有引发争议的设计。',
        '视觉识别系统从设计之初就刻意减少冲突感：印象派插画和柔和渐变是常见元素，它们不是为了讲清什么道理，而是要营造一种大众都能接受、不会得罪任何人的氛围。',
        '照片风格走的是人性化、接地气路线，让品牌看起来友好、沉稳又可靠。最终呈现的效果是：有权威但不傲慢，有领导力但不尖锐。',
    ]),
    ("2、温柔人文主义者", [
        '微软 AI、Notion 和 Anthropic 这类品牌都秉持以人为本的理念。',
        '品牌调性柔和，甚至带点浪漫感：视觉设计偏向人文，常用手绘插画呈现日常瞬间、自然景象和人际互动，画风活泼，有时甚至带点童真。',
        '它们刻意避开所有冰冷、硬核或可能引发不安的元素，让技术始终隐于幕后。',
        '真正重要的是：<strong>人们能用它做什么？它如何融入生活？又能带来怎样的体验？AI 是激发人类潜能的工具，而非让人畏惧的力量。</strong>',
    ]),
    ("3、理工理想主义者", [
        'Sakana、Midjourney、Mistral 这类品牌，骨子里不是商业驱动，而是对一项迷人技术的探索。它们的品牌基因里，浸透着工程文化和极客梗：故意做得不精致，有时玩心过重，有时奇奇怪怪，甚至故意不带品牌痕迹。',
        '那些不完美的"毛刺"，本身就是一种信号。它们不想把自己包装成严肃的企业超级品牌，目标也不是吸引普通消费者，而是同行：那些真正关心技术本身，而非跟风炒作的开发者、研究者和爱好者。',
    ]),
    ("4、大胆构建者", [
        '像 X AI、Intercom 和 Retool 这样的品牌，不把 AI 仅仅当作又一项技术，而是真正具有突破性的存在。',
        '他们不会试图弱化或人性化 AI 的力量，反而会主动拥抱这种力量。',
        '他们的品牌让 AI 显得宏大、强大且富有变革性：太空元素是常见的设计语言；用"最后的边界"来隐喻 AI 的无限可能；深色的调色板取代了米白和浅粉等柔和色调；少了些舒适感，多了份野心。',
        '这些品牌将 AI 定位为重塑可能性的力量，而非需要被"驯服"的工具。',
    ]),
    ("5、乌托邦梦想家", [
        'Perplexity、World Labs、Manus 这类品牌，很少谈论技术本身，更多聚焦于技术能带来的可能性。',
        '它们构建出宏大的创意世界：有时带着复古未来主义的韵味，有时又充满超现实感。',
        '传递的乐观乌托邦愿景或许会让部分受众困惑甚至感到疏离，但几乎总能引人入胜。比起清晰易懂，想象力才是关键。这无关当下，而是关乎那些尚未被定义的未来。',
        '这些品牌邀请人们先畅想，再理解：AI 不是渐进式进步的工具，而是催生全新现实的催化剂。',
    ]),
]

for title, paragraphs in archetypes:
    parts.append(h2(title))
    for text in paragraphs:
        parts.append(p(text))
    parts.append(img())  # each archetype has one image

# Closing
parts.append(hr())
parts.append(bold_p('最后，亲爱的读者。'))
parts.append(p('等你读完这篇文章时，里面有些内容大概率已经过时了。'))
parts.append(p('我们分析过的某些品牌，说不定已经消失了。'))
parts.append(p('但这恰恰是这个行业最迷人的地方：'))
parts.append(bold_p('单靠品牌建设赢不了，但一个能脱颖而出的品牌，能在这场争夺注意力、话语权和资本的激烈角逐中占据显著优势。'))
parts.append(p('原文：<a href="https://www.acolorbright.com/en/insights/aesthetics-of-ai" style="color: #576b95; text-decoration: underline;">https://www.acolorbright.com/en/insights/aesthetics-of-ai</a>'))
parts.append(p('更多美学文章 Insights 可访问网站：<a href="https://acolorbright.com/insights" style="color: #576b95; text-decoration: underline;">acolorbright.com/insights</a>'))

parts.append('</body></html>')

with open('article.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(parts))

print(f"Generated article.html with {img_idx[0]} image placeholders")
