# AWS Lightsail 部署指南

## 📋 準備工作

### 你需要：
1. ✅ AWS帳號
2. ✅ Telegram Bot Token（去 @BotFather 攞）
3. ✅ OneAccess API Key（你已經有：`sk-xxxxxxxx`）

---

## 🚀 部署步驟

### 步驟1：創建Lightsail實例

1. **登入AWS控制台**
   - 去 https://lightsail.aws.amazon.com

2. **創建實例**
   - 點 **"Create instance"**
   - 選擇地區：**Singapore** 或 **Tokyo**（亞洲最近）
   
3. **選擇系統**
   - Platform: **Linux/Unix**
   - Blueprint: **OS Only** → **Ubuntu 22.04 LTS**

4. **選擇計劃**
   - 選最平嘅：**$3.50/月**
   - 包括：
     - 512 MB RAM
     - 1 vCPU
     - 20 GB SSD
     - 1 TB transfer

5. **命名實例**
   - Instance name: `telegram-bot`

6. **點 "Create instance"**
   - 等1-2分鐘創建完成

---

### 步驟2：連接到服務器

1. **喺Lightsail控制台**
   - 點你啱啱創建嘅 `telegram-bot` 實例

2. **點 "Connect using SSH"**
   - 會打開一個瀏覽器terminal

3. **或者用自己嘅terminal（推薦）**
   - 下載SSH key
   - 點 "Account" → "SSH keys" → Download
   
   然後喺你電腦terminal：
   ```bash
   chmod 400 ~/Downloads/LightsailDefaultKey-ap-southeast-1.pem
   ssh -i ~/Downloads/LightsailDefaultKey-ap-southeast-1.pem ubuntu@你的IP地址
   ```

---

### 步驟3：部署機械人

連接到服務器之後，運行：

```bash
# 下載部署腳本
wget https://raw.githubusercontent.com/eugeniatsanget-ctrl/chickenfurbot/main/deploy_lightsail.sh

# 執行部署
chmod +x deploy_lightsail.sh
./deploy_lightsail.sh
```

腳本會問你輸入：
- Telegram Bot Token
- OneAccess API Key

---

### 步驟4：驗證運行

```bash
# 查看機械人狀態
sudo systemctl status telegram-bot

# 查看日誌
sudo journalctl -u telegram-bot -f
```

應該見到：`✅ 機械人已啟動！`

---

## 🎯 測試機械人

1. 去Telegram搵你個bot
2. 發送 `/start`
3. 試下傾偈

---

## 🔧 常用管理指令

```bash
# 查看狀態
sudo systemctl status telegram-bot

# 查看日誌（實時）
sudo journalctl -u telegram-bot -f

# 重啟機械人
sudo systemctl restart telegram-bot

# 停止機械人
sudo systemctl stop telegram-bot

# 啟動機械人
sudo systemctl start telegram-bot

# 更新代碼
cd ~/chickenfurbot
git pull
sudo systemctl restart telegram-bot
```

---

## 💰 費用

- **每月固定**：$3.50 USD
- **OneAccess API**：按使用量
- **總計**：~$3.50-5/月

---

## 🔒 安全建議

### 1. 設置防火牆
```bash
# 只開放SSH
sudo ufw allow 22
sudo ufw enable
```

### 2. 定期更新
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. 保護.env文件
```bash
chmod 600 ~/chickenfurbot/.env
```

---

## 🆘 常見問題

### Q: 機械人冇反應？
```bash
# 檢查日誌睇錯誤
sudo journalctl -u telegram-bot -n 50
```

### Q: 點樣更新代碼？
```bash
cd ~/chickenfurbot
git pull
sudo systemctl restart telegram-bot
```

### Q: 點樣改環境變量？
```bash
nano ~/chickenfurbot/.env
# 改完之後
sudo systemctl restart telegram-bot
```

### Q: 想停止服務？
```bash
sudo systemctl stop telegram-bot
sudo systemctl disable telegram-bot
```

---

## 📊 監控

### 查看系統資源
```bash
# CPU/記憶體使用
htop

# 磁碟空間
df -h

# 網絡流量
vnstat
```

---

## 🔄 自動備份對話記錄

```bash
# 創建備份腳本
cat > ~/backup.sh << 'EOF'
#!/bin/bash
cd ~/chickenfurbot
tar -czf backup-$(date +%Y%m%d).tar.gz conversation_history/
# 保留最近7天
find . -name "backup-*.tar.gz" -mtime +7 -delete
EOF

chmod +x ~/backup.sh

# 設置每日備份（凌晨3點）
(crontab -l 2>/dev/null; echo "0 3 * * * ~/backup.sh") | crontab -
```

---

## ✅ 完成！

你嘅Telegram機械人而家24/7喺AWS Lightsail度運行緊！

有問題隨時問我 🚀
