import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from openai import OpenAI
import json
from pathlib import Path

# 設置日誌
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 初始化OpenAI客戶端（OneAccess API）
client = OpenAI(
    api_key=os.environ.get("ONEACCESS_API_KEY"),
    base_url="https://oneaccessai.com/v1"
)

# 用戶對話歷史
user_conversations = {}

# 對話歷史文件夾
HISTORY_DIR = Path("conversation_history")
HISTORY_DIR.mkdir(exist_ok=True)


def load_user_history(user_id: int) -> list:
    """從文件加載用戶對話歷史"""
    history_file = HISTORY_DIR / f"user_{user_id}.json"
    if history_file.exists():
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"載入歷史失敗: {e}")
    return []


def save_user_history(user_id: int, history: list):
    """保存用戶對話歷史到文件"""
    history_file = HISTORY_DIR / f"user_{user_id}.json"
    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存歷史失敗: {e}")


def get_conversation_history(user_id: int) -> list:
    """獲取用戶對話歷史"""
    if user_id not in user_conversations:
        user_conversations[user_id] = load_user_history(user_id)
    return user_conversations[user_id]


def add_to_history(user_id: int, role: str, content: str):
    """添加消息到對話歷史"""
    history = get_conversation_history(user_id)
    history.append({"role": role, "content": content})

    # 保持最近50條對話
    if len(history) > 100:
        history = history[-100:]

    user_conversations[user_id] = history
    save_user_history(user_id, history)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理/start命令"""
    user = update.effective_user
    welcome_message = (
        f"你好 {user.mention_html()}！👋\n\n"
        "我係一個由AI驅動嘅機械人。你可以：\n\n"
        "💬 直接同我傾偈\n"
        "🖼️ 發圖片俾我分析\n"
        "🎤 發語音訊息\n"
        "📝 我會記住我哋嘅對話\n\n"
        "指令：\n"
        "/start - 開始\n"
        "/clear - 清除對話記錄\n"
        "/help - 幫助"
    )
    await update.message.reply_html(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理/help命令"""
    help_text = (
        "📖 <b>使用方法</b>\n\n"
        "直接打字或發語音，我就會回覆你。\n\n"
        "<b>指令列表：</b>\n"
        "/start - 開始使用\n"
        "/clear - 清除對話記錄\n"
        "/help - 顯示此幫助\n\n"
        "<b>支援功能：</b>\n"
        "✅ 文字對話\n"
        "✅ 圖片分析\n"
        "✅ 語音訊息\n"
        "✅ 記住對話上下文"
    )
    await update.message.reply_html(help_text)


async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """清除用戶對話歷史"""
    user_id = update.effective_user.id
    user_conversations[user_id] = []
    save_user_history(user_id, [])
    await update.message.reply_text("✅ 已清除對話記錄")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理文字消息"""
    user_id = update.effective_user.id
    user_message = update.message.text

    # 發送"正在輸入"狀態
    await update.message.chat.send_action(action="typing")

    # 添加用戶消息到歷史
    add_to_history(user_id, "user", user_message)

    try:
        # 調用OneAccess API
        response = client.chat.completions.create(
            model="claude-3-5-sonnet-20241022",  # OneAccess支援的模型
            messages=get_conversation_history(user_id),
            max_tokens=2048
        )

        # 獲取回覆
        assistant_message = response.choices[0].message.content

        # 添加助手回覆到歷史
        add_to_history(user_id, "assistant", assistant_message)

        # 發送回覆
        await update.message.reply_text(assistant_message)

    except Exception as e:
        logger.error(f"API調用錯誤: {e}")
        await update.message.reply_text(
            f"❌ 抱歉，發生錯誤：{str(e)}\n\n"
            "請檢查你嘅API key或稍後重試。"
        )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理圖片消息"""
    user_id = update.effective_user.id

    await update.message.chat.send_action(action="typing")

    try:
        # 獲取圖片
        photo = update.message.photo[-1]  # 最高質量
        photo_file = await photo.get_file()

        # 下載圖片
        photo_path = f"temp_{user_id}.jpg"
        await photo_file.download_to_drive(photo_path)

        # 讀取圖片為base64
        import base64
        with open(photo_path, "rb") as image_file:
            image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")

        # 獲取圖片說明（如果有）
        caption = update.message.caption or "請分析呢張圖片"

        # 準備消息（使用OpenAI vision格式）
        messages = get_conversation_history(user_id)
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": caption
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}"
                    }
                }
            ]
        })

        # 調用API
        response = client.chat.completions.create(
            model="claude-3-5-sonnet-20241022",
            messages=messages,
            max_tokens=2048
        )

        assistant_message = response.choices[0].message.content

        # 添加到歷史（簡化版）
        add_to_history(user_id, "user", f"[圖片] {caption}")
        add_to_history(user_id, "assistant", assistant_message)

        await update.message.reply_text(assistant_message)

        # 刪除臨時文件
        os.remove(photo_path)

    except Exception as e:
        logger.error(f"圖片處理錯誤: {e}")
        await update.message.reply_text(
            f"❌ 圖片處理失敗：{str(e)}\n\n"
            "可能係模型唔支援圖片分析。"
        )


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理語音消息"""
    user_id = update.effective_user.id

    await update.message.chat.send_action(action="typing")

    try:
        # 獲取語音文件
        voice = update.message.voice
        voice_file = await voice.get_file()

        # 下載語音
        voice_path = f"temp_voice_{user_id}.ogg"
        await voice_file.download_to_drive(voice_path)

        # 提示用戶
        await update.message.reply_text(
            "🎤 收到語音訊息！\n\n"
            "註：語音轉文字功能需要額外設置。\n"
            "暫時請用文字同我傾偈 😊"
        )

        # 刪除臨時文件
        os.remove(voice_path)

    except Exception as e:
        logger.error(f"語音處理錯誤: {e}")
        await update.message.reply_text(f"❌ 語音處理失敗：{str(e)}")


def main():
    """啟動機械人"""
    # 檢查環境變量
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    oneaccess_key = os.environ.get("ONEACCESS_API_KEY")

    if not telegram_token:
        print("❌ 錯誤：未設置 TELEGRAM_BOT_TOKEN")
        print("請設置環境變量")
        return

    if not oneaccess_key:
        print("❌ 錯誤：未設置 ONEACCESS_API_KEY")
        print("請設置環境變量")
        return

    print("🤖 正在啟動Telegram機械人...")
    print(f"📡 使用OneAccess API: https://oneaccessai.com/v1")

    # 創建應用
    application = Application.builder().token(telegram_token).build()

    # 添加處理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_history))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))

    # 啟動機械人
    print("✅ 機械人已啟動！")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
