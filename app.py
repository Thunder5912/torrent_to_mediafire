import os
import logging
import tempfile
from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN
from mediafire_uploader import upload_to_mediafire
from urllib.request import urlretrieve

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a torrent file or a direct download link.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.document:
        file = await update.message.document.get_file()
        with tempfile.NamedTemporaryFile(delete=False, suffix='.torrent') as temp:
            await file.download_to_drive(custom_path=temp.name)
            mediafire_link = upload_to_mediafire(temp.name)
            await update.message.reply_text(f"Uploaded to MediaFire:\n{mediafire_link}")
    elif update.message.text and update.message.text.startswith("http"):
        url = update.message.text
        filename = os.path.join(tempfile.gettempdir(), os.path.basename(url.split('?')[0]))
        urlretrieve(url, filename)
        mediafire_link = upload_to_mediafire(filename)
        await update.message.reply_text(f"Uploaded to MediaFire:\n{mediafire_link}")
    else:
        await update.message.reply_text("Please send a valid torrent file or download link.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_message))

if __name__ == "__main__":
    app.run_polling()
