#!/bin/bash

echo "🧪 本地測試機械人"
echo ""

# 檢查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未安裝Python 3"
    exit 1
fi

echo "✅ Python: $(python3 --version)"
echo ""

# 安裝依賴
echo "📦 安裝依賴..."
pip3 install -r requirements.txt
echo ""

# 提示輸入tokens
echo "🔑 請輸入你嘅tokens："
echo ""
read -p "Telegram Bot Token: " BOT_TOKEN
read -p "OneAccess API Key: " API_KEY

echo ""
echo "🚀 啟動機械人..."
echo ""

# 設置環境變量並運行
export TELEGRAM_BOT_TOKEN="$BOT_TOKEN"
export ONEACCESS_API_KEY="$API_KEY"

python3 bot.py
