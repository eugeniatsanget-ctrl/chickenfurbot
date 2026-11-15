# Telegram AI Bot (OneAccess API)

用OneAccess AI驅動嘅Telegram機械人，支援文字對話、圖片分析。

## 功能

- 💬 智能對話（使用Claude 3.5 Sonnet）
- 🖼️ 圖片分析
- 📝 記住對話歷史
- 🌐 24/7運行（部署到雲端）

## 快速開始

### 步驟1：攞Telegram Bot Token

1. 喺Telegram搵 `@BotFather`
2. 發送 `/newbot`
3. 跟住指示創建機械人
4. 保存token（格式：`123456789:ABCdefGHI...`）

### 步驟2：準備OneAccess API Key

- 你已經有：`sk-xxxxxxxx`
- API地址：`https://oneaccessai.com/v1`

### 步驟3：部署到Railway（免費24/7運行）

#### 方法A：網頁部署（最簡單）

1. **去Railway註冊**
   - 網址：https://railway.app
   - 用GitHub帳號登入

2. **創建新項目**
   - 點 "New Project"
   - 選 "Deploy from GitHub repo"
   - 連接呢個項目

3. **設置環境變量**
   點 "Variables" 添加：
   ```
   TELEGRAM_BOT_TOKEN = 你的telegram_token
   ONEACCESS_API_KEY = sk-xxxxxxxx
   ```

4. **完成！**
   - Railway會自動部署
   - 幾分鐘後機械人就會上線

#### 方法B：本地測試先

```bash
# 安裝依賴
pip3 install -r requirements.txt

# 設置環境變量（只係測試用）
export TELEGRAM_BOT_TOKEN="你的token"
export ONEACCESS_API_KEY="sk-xxxxxxxx"

# 運行
python3 bot.py
```

測試OK就push上GitHub再用方法A部署。

## 使用機械人

1. 喺Telegram搵到你嘅機械人
2. 發送 `/start` 開始
3. 直接打字同佢傾偈
4. 發圖片俾佢分析

## 指令

- `/start` - 開始使用
- `/help` - 顯示幫助
- `/clear` - 清除對話記錄

## Railway部署詳細步驟

### 第一次部署

1. **Fork呢個項目到你GitHub**
   - 去你個GitHub
   - 創建新repository
   - Upload呢啲文件

2. **連接Railway**
   ```
   1. https://railway.app → New Project
   2. Deploy from GitHub repo
   3. 選你個repo
   4. Add variables:
      - TELEGRAM_BOT_TOKEN
      - ONEACCESS_API_KEY
   5. Deploy
   ```

3. **檢查運行狀態**
   - 去 "Deployments" 睇logs
   - 應該見到 "✅ 機械人已啟動！"

### 其他部署選項

#### Render（完全免費但會sleep）

1. 去 https://render.com
2. New → Web Service
3. Connect GitHub repo
4. 設置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python3 bot.py`
5. 添加環境變量

#### VPS部署（最穩定）

```bash
# SSH到你VPS
ssh user@your-server

# 安裝依賴
sudo apt update
sudo apt install python3 python3-pip git

# Clone代碼
git clone your-repo-url
cd tg-bot

# 安裝Python包
pip3 install -r requirements.txt

# 設置環境變量（永久）
echo 'export TELEGRAM_BOT_TOKEN="你的token"' >> ~/.bashrc
echo 'export ONEACCESS_API_KEY="sk-xxx"' >> ~/.bashrc
source ~/.bashrc

# 用screen長期運行
screen -S bot
python3 bot.py
# 按 Ctrl+A 然後 D 離開
```

## 故障排除

### 機械人無反應
1. 檢查Railway logs有冇錯誤
2. 確認環境變量設置正確
3. 試下 `/start` 指令

### API錯誤
- 確認OneAccess API key有效
- 檢查額度有冇用完
- 睇logs嘅具體錯誤訊息

### Railway免費額度
- 每月$5免費credit
- 足夠跑一個輕量機械人
- 用完可以upgrade

## 費用估計

- Railway免費tier：每月$5 credit（夠用）
- OneAccess API：按使用量收費
- Render免費tier：完全免費但會sleep

## 更新機械人

```bash
# 改code
# Git push

# Railway會自動重新部署
```

## 注意事項

- 對話歷史保存在雲端（Railway會persist）
- 每個用戶最多100條對話記錄
- 圖片分析睇OneAccess支唔支援vision
- 24/7運行免費（Railway/Render）
