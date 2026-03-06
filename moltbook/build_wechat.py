#!/usr/bin/env python3
"""
从飞书文档提取图片并生成公众号可用的 HTML
用法: python3 build_wechat.py
前提: 已在 Chrome 中登录飞书并能访问该文档
"""
import urllib.request
import base64
import os
import re
import ssl

# 飞书图片 tokens（按文档中出现顺序）
IMAGE_TOKENS = [
    "Q03dbqOpyoECzvxPk5Dc3wv5nSb",
    "IQBRbLxeUotpfUxvZZRcBFyEnIW",
    "FRUTbirjyohylMxV3ricH5kjnlb",
    "JPAGbLrX4o5v5NxQCNkcK2Ann1e",
    "OHkhbwcuIo6Z0bxqvxocUAmInEh",
    "EIlwbTS2ho42cbxwwurcW680nff",
    "Px2ObUbLwoaqCZxl6hacSJ6cnCg",
    "DduvbeU9aoHOQ1xZGYWcBs96nXf",
    "SWmybWugAozJ0sxNPK0cUoU7nch",
    "DvSGbRHZAorWQ6xkVFDcKLSwnA3",
    "SjchbgMoBoHJV0x7Qz7c89hjnJb",
    "Zrjtbq4d0oKQ5lxK3ALc9pddnyd",
    "STqabuJgYoaiynxKp2Ic8dJYncb",
    "K96XbPpKLoxoWrxtQajcYa1vnUf",
    "Z7TjbYQ3aoYJ26xVBKrcVJwPnVe",
]

os.makedirs("images", exist_ok=True)

print("=" * 60)
print("飞书文档 → 公众号 HTML 转换工具")
print("=" * 60)
print()
print("此工具需要你手动将 15 张图片保存到 images/ 目录。")
print()
print("最快捷的操作方式：")
print("1. 在浏览器中打开飞书文档")
print("2. 右键每张图片 → 另存为")
print("3. 按 img1.png ~ img15.png 命名保存到 images/ 目录")
print()

# 检查图片文件
found = 0
for i in range(1, 16):
    for ext in ['png', 'jpg', 'jpeg', 'webp']:
        path = f"images/img{i}.{ext}"
        if os.path.exists(path):
            found += 1
            break

if found < 15:
    print(f"⚠️  当前找到 {found}/15 张图片")
    print("   请先保存所有图片后重新运行此脚本")
    print()
    # 继续生成，缺失的图片用占位符
else:
    print(f"✅ 所有 15 张图片已就绪！")

# 读取 HTML 模板
with open("article.html", "r", encoding="utf-8") as f:
    html = f.read()

# 替换图片为 base64 内嵌或本地路径
for i in range(1, 16):
    placeholder = f"IMG_PLACEHOLDER_{i}"
    img_path = None
    for ext in ['png', 'jpg', 'jpeg', 'webp']:
        path = f"images/img{i}.{ext}"
        if os.path.exists(path):
            img_path = path
            break

    if img_path:
        # 转为 base64 内嵌（公众号友好）
        with open(img_path, "rb") as f:
            data = f.read()
        ext = img_path.rsplit('.', 1)[1]
        mime = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'webp': 'image/webp'}[ext]
        b64 = base64.b64encode(data).decode()
        html = html.replace(placeholder, f"data:{mime};base64,{b64}")
        print(f"  ✅ img{i} → base64 内嵌")
    else:
        print(f"  ⚠️  img{i} 未找到，保留占位符")

# 写入最终 HTML
with open("article_final.html", "w", encoding="utf-8") as f:
    f.write(html)

print()
print("=" * 60)
print("✅ 生成完毕: article_final.html")
print()
print("使用方法：")
print("  1. 在浏览器中打开 article_final.html")
print("  2. Cmd+A 全选 → Cmd+C 复制")
print("  3. 粘贴到公众号后台编辑器")
print("  4. 图片会自动上传到公众号素材库")
print("=" * 60)
