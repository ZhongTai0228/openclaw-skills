import re

with open('article_v2.html', 'r') as f:
    html = f.read()

# 1. Date headers: change from centered h2 to left-aligned bold paragraph
# These are the 17px ones with dates
date_h2_pattern = r'<h2 style="text-align: center; line-height: 2em; margin-bottom: 24px; margin-left: 8px; margin-right: 8px;"><span style="color: rgb\(30, 30, 30\); font-family: \'PingFang SC\', system-ui, -apple-system, \'Helvetica Neue\', \'Hiragino Sans GB\', \'Microsoft YaHei UI\', \'Microsoft YaHei\', Arial, sans-serif; font-size: 17px; letter-spacing: 1px;"><span style="font-weight: bold;">(\d+ 月 \d+ 日)</span></span></h2>'

def date_replacement(m):
    date = m.group(1)
    return f'<p style="line-height: 2em; margin-bottom: 24px; margin-left: 8px; margin-right: 8px; text-align: justify;"><span style="color: rgb(30, 30, 30); font-family: \'PingFang SC\', system-ui, -apple-system, \'Helvetica Neue\', \'Hiragino Sans GB\', \'Microsoft YaHei UI\', \'Microsoft YaHei\', Arial, sans-serif; font-size: 17px; letter-spacing: 1px;"><strong>{date}</strong></span></p>'

html = re.sub(date_h2_pattern, date_replacement, html)

# 2. Replace western quotes with Chinese quotes「」
# Pattern: 「...」 already Chinese - good
# But check for "" style quotes
# Looking at content: uses 「」 already in some places, and "" in others
# Replace "..." with "..."
html = html.replace('\u201c', '\u300c')  # " -> 「
html = html.replace('\u201d', '\u300d')  # " -> 」

# 3. Fix bullet list items - currently ugly with · prefix and margin-left:24px
# Make them look like proper indented items with better spacing
old_list_style = 'line-height: 2em; margin-bottom: 8px; margin-left: 24px; margin-right: 8px;'
new_list_style = 'line-height: 2em; margin-bottom: 12px; margin-left: 16px; margin-right: 8px; text-indent: -0.8em; padding-left: 0.8em; text-align: justify;'
html = html.replace(old_list_style, new_list_style)

# Fix the last item in each list (24px bottom margin)
old_last_item = 'line-height: 2em; margin-bottom: 24px; margin-left: 24px; margin-right: 8px;'
new_last_item = 'line-height: 2em; margin-bottom: 24px; margin-left: 16px; margin-right: 8px; text-indent: -0.8em; padding-left: 0.8em; text-align: justify;'
html = html.replace(old_last_item, new_last_item)

# 4. Make sure all regular paragraphs have text-align: justify (some might not)
# The italic quote paragraphs don't have it - add it
html = html.replace('font-style: italic;">', 'font-style: italic; text-align: justify;">')

with open('article_v2.html', 'w') as f:
    f.write(html)

print("Done! Changes applied.")
