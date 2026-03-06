#!/bin/bash
# 从飞书文档下载图片并生成带图 HTML
# 用法：在浏览器中打开飞书文档后运行此脚本

cd "$(dirname "$0")"
mkdir -p images

echo "请手动从飞书文档中保存15张图片到 $(pwd)/images/ 目录下"
echo "命名为 img1.png 到 img15.png"
echo ""
echo "图片对应关系："
echo "  img1  - 题图（大横幅图）"
echo "  img2  - 第一个分隔线"
echo "  img3  - MOLT代币走势图（2月2日后）"
echo "  img4  - 沉默配图（2月8日后）"
echo "  img5  - Peter Steinberger（2月15日）"
echo "  img6  - OpenClaw 截图"
echo "  img7  - 推文截图（Sam Altman）"
echo "  img8  - 空城配图（2月21日后）"
echo "  img9  - 第二个分隔线"
echo "  img10 - 插图（创始人轨迹后）"
echo "  img11 - 插图（系统内部观察后）"
echo "  img12 - 第三个分隔线"
echo "  img13 - 尾图1（署名后）"
echo "  img14 - 尾图2"
echo "  img15 - 尾图3"
echo ""

# 替换 HTML 中的占位符
sed 's|IMG_PLACEHOLDER_1|images/img1.png|g; s|IMG_PLACEHOLDER_2|images/img2.png|g; s|IMG_PLACEHOLDER_3|images/img3.png|g; s|IMG_PLACEHOLDER_4|images/img4.png|g; s|IMG_PLACEHOLDER_5|images/img5.png|g; s|IMG_PLACEHOLDER_6|images/img6.png|g; s|IMG_PLACEHOLDER_7|images/img7.png|g; s|IMG_PLACEHOLDER_8|images/img8.png|g; s|IMG_PLACEHOLDER_9|images/img9.png|g; s|IMG_PLACEHOLDER_10|images/img10.png|g; s|IMG_PLACEHOLDER_11|images/img11.png|g; s|IMG_PLACEHOLDER_12|images/img12.png|g; s|IMG_PLACEHOLDER_13|images/img13.png|g; s|IMG_PLACEHOLDER_14|images/img14.png|g; s|IMG_PLACEHOLDER_15|images/img15.png|g' article.html > article_final.html

echo "✅ 生成完毕: article_final.html"
echo "在浏览器中打开后 Cmd+A 全选，Cmd+C 复制，粘贴到公众号后台即可"
