#!/usr/bin/env bash
# ensure_chrome_cdp.sh - 确保 Chrome 以 CDP 调试端口运行
#
# 用法: ./ensure_chrome_cdp.sh [port]
# 默认端口: 9222

PORT="${1:-9222}"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DATA_DIR="/tmp/chrome-watcha-cdp"

# 检查端口是否已在监听
if curl -s "http://127.0.0.1:$PORT/json/version" > /dev/null 2>&1; then
  echo '{"status":"already_running","port":'$PORT'}'
  exit 0
fi

# 关闭已有 Chrome 实例
pkill -9 -f "Google Chrome" 2>/dev/null
sleep 2

# 启动带调试端口的 Chrome
nohup "$CHROME" \
  --remote-debugging-port="$PORT" \
  --user-data-dir="$DATA_DIR" \
  --no-first-run \
  "https://watcha.cn/square/discuss" \
  > /dev/null 2>&1 &

# 等待启动
for i in $(seq 1 10); do
  sleep 1
  if curl -s "http://127.0.0.1:$PORT/json/version" > /dev/null 2>&1; then
    echo '{"status":"started","port":'$PORT',"data_dir":"'$DATA_DIR'"}'
    echo "⚠️  This is a fresh Chrome profile. You need to log in to watcha.cn manually." >&2
    exit 0
  fi
done

echo '{"status":"failed","error":"Chrome did not start with CDP in time"}' >&2
exit 1
