import os
import json
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

# Завантаження змінних із .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in the .env file")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Канали для публікації
CHANNELS = {
    "uk": "@your_ukrainian_channel",
    "de": "@your_german_channel",
    "ru": "@your_russian_channel"
}

# Розбиває повідомлення, якщо воно перевищує 4096 символів
def split_message(message, max_length=4096):
    if len(message) <= max_length:
        return [message]
    parts = []
    while len(message) > max_length:
        split_index = message.rfind("\n", 0, max_length)
        if split_index == -1:
            split_index = max_length
        parts.append(message[:split_index])
        message = message[split_index:].strip()
    parts.append(message)
    return parts

# Функція для публікації новин
def publish_news(input_file, language):
    if not os.path.exists(input_file):
        print(f"❌ Translation file {input_file} not found.")
        return

    channel = CHANNELS.get(language)
    if not channel:
        print(f"❌ No channel specified for language: {language}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        news_items = json.load(f)

    published_count = 0
    for index, item in enumerate(news_items, start=1):
        try:
            message = (
                f"📢 {item['original']['title']}\n\n"
                f"{item['translation']}\n\n"
                f"🔗 {item['original']['link']}"
            )
            for part in split_message(message):
                bot.send_message(chat_id=channel, text=part)
            published_count += 1
            print(f"✅ Published to {channel}: {item['original']['title']}")
        except TelegramError as e:
            print(f"❌ Error publishing item {index} to {channel}: {e}")

    print(f"🔔 Finished publishing to {channel}. {published_count}/{len(news_items)} items published.")

if __name__ == "__main__":
    TRANSLATION_FILES = {
        "uk": "translations_uk.json",
        "de": "translations_de.json",
        "ru": "translations_ru.json"
    }
    for lang, file in TRANSLATION_FILES.items():
        publish_news(file, lang)
