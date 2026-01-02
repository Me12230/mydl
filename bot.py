from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import os

# ======= فقط توکن لازم هست =======
TOKEN = "8363711566:AAEZ8M2C_4cskOWKQzT31w0WMgNsu7ZKn10"

# دستور /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "سلام! 👋\nلینک اینستاگرام رو برام بفرست تا ویدیو یا عکسش رو دانلود کنم."
    )

# دریافت لینک و دانلود از اینستاگرام
def handle_message(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    if "instagram.com" not in url:
        update.message.reply_text("این لینک اینستاگرام نیست! دوباره امتحان کن.")
        return

    try:
        # استفاده از سایت دانلود واسط رایگان
        api_url = f"https://api.v1.instadl.com/?url={url}"
        r = requests.get(api_url).json()
        media_url = r['media_url']
        media_type = r['media_type']

        # دانلود فایل
        filename = "media.mp4" if media_type == "video" else "media.jpg"
        media_data = requests.get(media_url).content
        with open(filename, "wb") as f:
            f.write(media_data)

        # ارسال به تلگرام
        if media_type == "video":
            update.message.reply_video(filename)
        else:
            update.message.reply_photo(filename)

        # حذف فایل بعد از ارسال
        os.remove(filename)

    except Exception as e:
        update.message.reply_text("مشکلی پیش اومد! مطمئن شو لینک درست باشه.")

# ======= راه‌اندازی ربات =======
updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling()
updater.idle()