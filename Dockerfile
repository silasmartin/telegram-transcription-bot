FROM python:3.11
LABEL Maintainer="Silas Martin <sm@akamo.de>" \
  Description="Telegram transcription bot for voice messages"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt update && apt install -y ffmpeg
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]