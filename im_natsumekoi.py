import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# --- 配置部分 ---
TELEGRAM_TOKEN = "8231619189:??HcwDu_X7aN3iNaA0XwikpwjAbyH_Zmgi0"
GOOGLE_API_KEY = "??zaSyAbSNEwXMNKQ4RBE_UeoQ23cCxEJ_SzVSY"

# 如果 Gemini 3 Pro 已发布，请在此处更改模型名称，例如 "gemini-3.0-pro"
# 目前常用的是 "gemini-1.5-pro-latest"
MODEL_NAME = "gemini-2.5-flash" 

# --- 初始化 Gemini ---
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# --- 定义回复逻辑 ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="你好！我是接入了 Gemini 的机器人。")

async def chat_with_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id

    # 显示“正在输入...”状态
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        # 发送给 Gemini 并获取回复
        response = model.generate_content(user_text)
        reply_text = response.text
        
        # 发送回复给 Telegram 用户
        # 注意：Telegram 单条消息限制 4096 字符，长回复可能需要切分
        await context.bot.send_message(chat_id=chat_id, text=reply_text)
        
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"出错了: {str(e)}")

# --- 主程序 ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # 添加处理程序
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat_with_gemini)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    print("机器人正在运行...")

    application.run_polling()
