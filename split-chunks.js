// Split base64 into chunks and create a loader script
const fs = require('fs');
const b64 = fs.readFileSync('/tmp/openclaw/uploads/section-b64.txt', 'utf8').trim();
const chunkSize = 10000;
const chunks = [];
for (let i = 0; i < b64.length; i += chunkSize) {
  chunks.push(b64.slice(i, i + chunkSize));
}
console.log('Total chunks: ' + chunks.length);
for (let i = 0; i < chunks.length; i++) {
  fs.writeFileSync(`/tmp/openclaw/uploads/chunk-${i}.txt`, chunks[i]);
}
