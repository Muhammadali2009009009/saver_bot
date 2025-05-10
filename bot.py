import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os

# 🔐 Bot token
BOT_TOKEN = '8125797436:AAHMXyNxIcJdJb9lbB22P9YcUDlikkLTMSY'

# 👤 Admin kontakt
ADMIN_CONTACT = 'https://t.me/Tech_nestCreator'

# 📋 Log sozlamasi
logging.basicConfig(level=logging.INFO)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom! YouTube yoki Instagram videosining linkini yuboring.\n\nKomandalar:\n/help - yordam\n/about - bot haqida")

# /help komandasi
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🛠 Yordam kerak bo‘lsa admin: {ADMIN_CONTACT}")

# /about komandasi
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📺 Bu bot YouTube videolarini yuklaydi.\nFoydalanish uchun video linkini yuboring.\nInstagram hozircha vaqtincha ishlamaydi.")

# YouTube videosini yuklovchi funksiya
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("📥 Yuklanmoqda, iltimos kuting...")

        try:
            ydl_opts = {
                'format': 'mp4',
                'outtmpl': 'video.%(ext)s',
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            video_file = next((f for f in os.listdir() if f.startswith("video") and f.endswith(".mp4")), None)

            if video_file:
                await update.message.reply_video(video=open(video_file, 'rb'))
                os.remove(video_file)
            else:
                await update.message.reply_text("❗ Video topilmadi yoki yuklab bo‘lmadi.")

        except Exception as e:
            await update.message.reply_text("❌ Video yuklashda xatolik yuz berdi.")
            print(f"Xato: {e}")

    elif "instagram.com" in url:
        await update.message.reply_text("📌 Instagram video yuklash vaqtincha cheklangan.")
    else:
        await update.message.reply_text("❗ Faqat YouTube yoki Instagram link yuboring.")

# Botni ishga tushuruvchi funksiya
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Komanda handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))

    # Faqat matn (link) bo‘lsa qabul qilish
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Botni ishga tushirish
    app.run_polling()

# ⏱ Ishga tushirish
if __name__ == "__main__":
    main()
