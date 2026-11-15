#!/bin/bash

echo "🚀 AWS Lightsail 部署腳本"
echo ""

# 更新系統
echo "📦 更新系統..."
sudo apt update
sudo apt upgrade -y

# 安裝Python和pip
echo "🐍 安裝Python..."
sudo apt install -y python3 python3-pip python3-venv

# 安裝Git
echo "📥 安裝Git..."
sudo apt install -y git

# Clone代碼
echo "📂 下載代碼..."
cd ~
git clone https://github.com/eugeniatsanget-ctrl/chickenfurbot.git
cd chickenfurbot

# 創建虛擬環境
echo "🔧 設置Python環境..."
python3 -m venv venv
source venv/bin/activate

# 安裝依賴
echo "📦 安裝依賴..."
pip install --upgrade pip
pip install -r requirements.txt

# 設置環境變量
echo ""
echo "🔑 請設置環境變量："
echo ""
read -p "請輸入 Telegram Bot Token: " BOT_TOKEN
read -p "請輸入 OneAccess API Key: " API_KEY

# 保存環境變量到.env文件
cat > .env << EOF
TELEGRAM_BOT_TOKEN=$BOT_TOKEN
ONEACCESS_API_KEY=$API_KEY
EOF

echo ""
echo "✅ 環境變量已保存到 .env 文件"
echo ""

# 創建systemd服務
echo "⚙️  創建系統服務..."
sudo tee /etc/systemd/system/telegram-bot.service > /dev/null << EOF
[Unit]
Description=Telegram AI Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/chickenfurbot
Environment="PATH=$HOME/chickenfurbot/venv/bin"
EnvironmentFile=$HOME/chickenfurbot/.env
ExecStart=$HOME/chickenfurbot/venv/bin/python3 $HOME/chickenfurbot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 啟動服務
echo "🔄 啟動機械人..."
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

echo ""
echo "✅ 部署完成！"
echo ""
echo "📋 常用指令："
echo "  查看狀態: sudo systemctl status telegram-bot"
echo "  查看日誌: sudo journalctl -u telegram-bot -f"
echo "  重啟服務: sudo systemctl restart telegram-bot"
echo "  停止服務: sudo systemctl stop telegram-bot"
echo ""
echo "🎉 你的機械人已經在運行！"
