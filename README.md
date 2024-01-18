# Telegram Transcription Bot

## Description

This bot uses [OpenAI's whisper](https://github.com/openai/whisper) and [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) to transcribe your voice messages and audio files from Telegram and other messengers like WhatsApp. You can just send the voice message to your Telegram-Bot and it responds with the containing text.

## Installation

### Docker

I recommend using Docker on a server to build and run this repository. To do this, run these commands **as root**:

1. Clone the repository & cd into it

```bash
git clone https://github.com/silasmartin/telegram-transcription-bot.git && cd telegram-transcription-bot
```

2. Edit the .env file and insert your token. You can get it via [BotFather](https://t.me/BotFather).

```bash
nano .env
```

3. Build the image

```bash
docker build . --tag ttbot
```

4. Run the image

```bash
docker run -d --restart unless-stopped ttbot
```

It takes a few moments to download the whisper model, depending on your internet speed. You could always check the status with docker logs.

### Local installation

You can run this on a local machine as well. Just clone the repository, edit .env, install requirements.txt with pip and run main.py - that's it!

## Need help?

I'm happy to take a look. [Reach out](https://t.me/silasmartin)!
