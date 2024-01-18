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
    print("Received voice message")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Received voice message, transcription running...",
    )

    # Get the voice message
    voice_message = update.message.voice or update.message.audio

    # Determine the file extension --> adds support for forwarding from WhatsApp
    file_extension = ".ogg"  # Default to .ogg for voice messages
    if update.message.voice:
        file_extension = ".ogg"
    elif update.message.audio:
        if update.message.audio.mime_type:
            mime_type = update.message.audio.mime_type
            if mime_type == "audio/mp4":
                file_extension = ".m4a"
            elif mime_type == "audio/mpeg":
                file_extension = ".mp3"

    file_path = f"./voice{file_extension}"

    # Download the file
    new_file = await context.bot.get_file(voice_message.file_id)
    await new_file.download_to_drive(custom_path=file_path)

    # Transcribe the audio file
    result = model.transcribe(file_path)
    # print(result["text"]) --> Privacy first
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=result["text"]
    )
    try:
        os.remove(file_path)
        print(f"Successfully deleted file: {file_path}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Successfully deleted voice message from server!",
        )
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Error while deleting the voice message from server - your file is still there! Contact the admin.",
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    transcription_handler = MessageHandler(filters.VOICE, transcribe)
    audio_handler = MessageHandler(filters.AUDIO, transcribe)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(transcription_handler)
    application.add_handler(audio_handler)

    application.run_polling()
