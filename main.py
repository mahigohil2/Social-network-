import telebot
from yt_dlp import YoutubeDL
import os

bot = telebot.TeleBot("7630522855:AAGCLFdD6RmEoli6sjzKKwPsl8v4-VqhoaI")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Send a short video link to download.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    bot.reply_to(message, "Downloading video, please wait...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file)

        os.remove(filename)
        bot.reply_to(message, "Video sent. Send another link if you want.")

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}. Send a valid link.")

bot.polling()
