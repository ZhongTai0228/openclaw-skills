// Script to extract section HTML and encode as base64
const fs = require('fs');
const html = fs.readFileSync('/tmp/openclaw/uploads/wechat-article.html', 'utf8');
const match = html.match(/<section class="container"[\s\S]*?<\/section>/);
if (match) {
  fs.writeFileSync('/tmp/openclaw/uploads/section-b64.txt', Buffer.from(match[0]).toString('base64'));
  console.log('OK, length: ' + match[0].length);
} else {
  console.log('NO MATCH');
}
