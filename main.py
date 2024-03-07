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
        parse_mode="MarkdownV2",
        chat_id=update.effective_chat.id,
        text="""
Hi there\! ✌️
            
I am a transcription bot designed to transcribe any voice message, video message and plain voice or video files you send me\. If you're interested in this project, look it up on [GitHub](https://github.com/silasmartin/telegram-transcription-bot)\.
            
I am using [Whisper](https://github.com/openai/whisper) and an awesome [open source Telegram bot package](https://github.com/python-telegram-bot/python-telegram-bot) under the hood\.

I was developed by [Silas Martin](tg://user?id=378380269), and he would love to hear your feedback\! So, if you're encountering any problems, just reach out\. 

⚠️ Disclaimer\: Although I always keep your and my own privacy in mind while developing software, I offer this experimental service for free to anybody who would like to use it, but I do not guarantee anything, including your privacy\. 
Use this bot at your own risk\!""",
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        parse_mode="MarkdownV2",
        chat_id=update.effective_chat.id,
        text=" Don't send me text \- I'll never know how to react to this\! 😬 Try voice or video messages instead\.",
    )


async def transcribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Received message")
    print(update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Received message, transcription running...",
    )

    # Get the voice message
    message_to_transcript = (
        update.message.voice
        or update.message.audio
        or update.message.video_note
        or update.message.video
    )

    file_path = "./voice"

    # Download the file
    new_file = await context.bot.get_file(message_to_transcript.file_id)
    await new_file.download_to_drive(custom_path=file_path)

    # Transcribe the audio file
    result = model.transcribe(file_path)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=result["text"]
    )
    try:
        os.remove(file_path)
        print(f"Successfully deleted file: {file_path}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Successfully deleted message from server!",
        )
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")
        await context.bot.send_message(
            parse_mode="MarkdownV2",
            chat_id=update.effective_chat.id,
            text="Error while deleting the message from server \- your file is still there! Contact the [admin](tg://user?id=378380269)\.",
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    transcription_handler = MessageHandler(filters.VOICE, transcribe)
    audio_handler = MessageHandler(filters.AUDIO, transcribe)
    video_handler = MessageHandler(filters.VIDEO, transcribe)
    video_note_handler = MessageHandler(filters.VIDEO_NOTE, transcribe)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(transcription_handler)
    application.add_handler(audio_handler)
    application.add_handler(video_handler)
    application.add_handler(video_note_handler)

    application.run_polling()
