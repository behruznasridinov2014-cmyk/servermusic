import asyncio
from multiprocessing.spawn import _main
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import yt_dlp

# Вставь свой токен сюда
API_TOKEN = '8792626553:AAEb9xz2nlQPCKoGNQC5IH8WygZ5ekpWQxw'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'default_search': 'ytsearch1',
    'outtmpl': 'song.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🎵 Привет! Скинь название песни или ссылку на YouTube!")

@dp.message()
async def handle_message(message: types.Message):
    query = message.text
    status = await message.answer(f"⏳ Ищу: {query}...")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            
            title = info.get('title', 'music_file')
            filename = 'song.mp3'

            audio_file = types.FSInputFile(filename)
            await message.answer_audio(audio_file, caption=f"✅ {title}")
            
            if os.path.exists(filename):
                os.remove(filename)
            await status.delete()

    except Exception as e:
        await message.answer(f"❌ Ошибка! Возможно, нужно установить ffmpeg.")
        print(f"Error: {e}")
async def main():
    print("🚀 БОТ ЗАПУЩЕН!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):       
        print("Бот выключен")      
from flask import Flask # pyright: ignore[reportMissingImports]
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
  app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def keep_alive():
    t = Thread(target=run)
    t.start()
from flask import Flask # pyright: ignore[reportMissingImports]
from threading import Thread
import os

# Создаем мини-сайт внутри бота
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

# Функция, которая запускает сервер на порту от Render
def run():
    # Вот тут мы используем тот самый PORT, который ты ввел в Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Запускаем сервер в отдельном потоке, чтобы он не мешал боту
def keep_alive():
    t = Thread(target=run)
    t.start()




                       