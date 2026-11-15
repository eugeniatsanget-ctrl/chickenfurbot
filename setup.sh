#!/bin/bash

echo "🚀 開始設置Telegram Bot..."

# 檢查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未安裝Python 3"
    exit 1
fi

echo "✅ Python已安裝: $(python3 --version)"

# 安裝依賴
echo "📦 正在安裝依賴..."
pip3 install -r requirements.txt

echo ""
echo "✅ 安裝完成！"
echo ""
echo "📝 下一步："
echo ""
echo "1. 去Telegram搵 @BotFather 攞bot token"
echo "2. 設置環境變量："
echo "   export TELEGRAM_BOT_TOKEN='你的token'"
echo "   export ANTHROPIC_API_KEY='你的api_key'"
echo ""
echo "3. 運行機械人："
echo "   python3 bot.py"
echo ""
