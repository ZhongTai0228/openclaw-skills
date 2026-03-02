#!/usr/bin/env python3
"""
Fix typography in a 公众号 HTML article:
1. Replace English straight quotes with Chinese curved quotes "" in text nodes
2. Add spaces between CJK and English/numbers (except near punctuation)
3. Remove spaces between English/numbers and CJK punctuation

Usage: python3 fix_typography.py <input.html> [output.html]
If output is omitted, modifies in place.
"""
import re
import sys

CN_PUNC = r'[，。！？：；、\u201c\u201d\u2018\u2019（）《》【】…—\u3001\u3002\uff0c\uff01\uff1f\uff1a\uff1b]'

def fix_quotes(text):
    """Replace paired straight quotes with Chinese curved quotes in a text node."""
    result = ''
    in_quote = False
    for ch in text:
        if ch == '"':
            result += '\u201c' if not in_quote else '\u201d'
            in_quote = not in_quote
        else:
            result += ch
    return result

def fix_cjk_spacing(text):
    """Add spaces between CJK and Latin/digits, remove spaces near CJK punctuation."""
    # Add space: CJK followed by Latin/digit
    text = re.sub(r'([\u4e00-\u9fff\u3400-\u4dbf])([A-Za-z0-9$@#(])', r'\1 \2', text)
    # Add space: Latin/digit followed by CJK
    text = re.sub(r'([A-Za-z0-9%\.\)\]\}!?])([\u4e00-\u9fff\u3400-\u4dbf])', r'\1 \2', text)
    # Remove space before CJK punctuation
    text = re.sub(r'([A-Za-z0-9%\.\)\]\}!?]) +(' + CN_PUNC + ')', r'\1\2', text)
    # Remove space after CJK punctuation
    text = re.sub(r'(' + CN_PUNC + r') +([A-Za-z0-9$@#(])', r'\1\2', text)
    return text

def process_html(html):
    """Process only text nodes (between > and <), preserving HTML tags."""
    parts = re.split(r'(<[^>]+>)', html)
    for i, part in enumerate(parts):
        if not part.startswith('<'):
            part = fix_quotes(part)
            part = fix_cjk_spacing(part)
            parts[i] = part
    return ''.join(parts)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 fix_typography.py <input.html> [output.html]')
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path
    
    with open(input_path, 'r') as f:
        html = f.read()
    
    html = process_html(html)
    
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f'Fixed typography: {input_path} -> {output_path}')
