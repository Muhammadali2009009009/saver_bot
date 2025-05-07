import logging
from pytube import YouTube
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import os

# Token va kanal sozlamalari
BOT_TOKEN = '8125797436:AAHMXyNxIcJdJb9lbB22P9YcUDlikkLTMSY'
CHANNEL_USERNAME = 'mygustili'  # Kanal usernamesi faqat @siz
ADMIN_CONTACT = 'https://t.me/Tech_nestCreator'

# Logging
logging.basicConfig(level=logging.INFO)

# Obuna tekshiruvi
async def check_subscription(user_id, context: ContextTypes.DEFAULT_TYPE):
    try:
        member = await context.bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
        return member.status in ['member', 'creator', 'administrator']
    except Exception:
        return False

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await check_subscription(user_id, context):
        await update.message.reply_text("🎉 Salom! Video silkasini yuboring.")
    else:
        keyboard = [
            [InlineKeyboardButton("📢 Kanalga a'zo bo'lish", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("✅ A'zo bo‘ldim", callback_data="check_sub")]
        ]
        await update.message.reply_text("Botdan foydalanish uchun kanalga a'zo bo‘ling 👇", reply_markup=InlineKeyboardMarkup(keyboard))

# A'zo bo‘ldim tugmasi
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if await check_subscription(user_id, context):
        await query.message.delete()
        await query.message.reply_text("🎉 Rahmat! Endi video silkasini yuboring.")
    else:
        await query.message.reply_text("❌ Siz hali kanalga a'zo bo‘lmagansiz.")

# YouTube yuklash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await check_subscription(user_id, context):
        return

    text = update.message.text
    if "youtube.com" in text or "youtu.be" in text:
        try:
            yt = YouTube(text)
            stream = yt.streams.get_highest_resolution()
            file_path = stream.download(filename="video.mp4")
            await update.message.reply_video(video=open(file_path, 'rb'), caption=yt.title)
            os.remove(file_path)
        except Exception as e:
            await update.message.reply_text("⚠️ Video yuklab bo‘lmadi.")
    elif "instagram.com" in text:
        await update.message.reply_text("📌 Instagram videoni yuklash imkoniyati hozirda vaqtincha cheklangan.")
    else:
        await update.message.reply_text("❗ Iltimos, faqat Instagram yoki YouTube silkasini yuboring.")

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Yordam kerak bo‘lsa admin: {ADMIN_CONTACT}")

# /about
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📺 Bu bot YouTube va Instagram videolarini yuklaydi.\nFoydalanish uchun video silkani yuboring.")

# Botni ishga tushirish
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
