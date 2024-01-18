import logging
import whisper
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

model = whisper.load_model("large")
load_dotenv()
TOKEN = os.getenv("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


async def transcribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("received voice message")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Received voice message, transcription running...",
    )
    new_file = await context.bot.get_file(update.message.voice.file_id)
    await new_file.download_to_drive(custom_path="./voice.ogg")
    result = model.transcribe("voice.ogg")
    print(result["text"])
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=result["text"]
    )


if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    start_handler = CommandHandler("start", start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    transcription_handler = MessageHandler(filters.VOICE, transcribe)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(transcription_handler)

    application.run_polling()
