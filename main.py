import time
from rss_parser import parse_rss, save_filtered_news  # Модуль для збору та збереження новин
from news_processor import process_news  # Модуль для обробки новин
from translator import translate_news  # Модуль для перекладу новин
from telegram_publisher import publish_news  # Модуль для публікації новин

# Інтервал перевірки новин у секундах (8 годин)
CHECK_INTERVAL = 8 * 3600

# Список RSS-джерел і ключових слів для фільтрації
RSS_FEED_URLS = [
    "https://openai.com/blog/rss",
    "https://ai.googleblog.com/feeds/posts/default",
    "https://qudata.com/uk/news-ai/rss",
    "https://www.unite.ai/feed/",
    "https://blog.colobridge.net/feed/"
]
KEYWORDS = ["AI", "artificial intelligence", "machine learning", "data science"]

# Шляхи до файлів для збереження результатів
RAW_NEWS_FILE = "filtered_data.json"  # Файл із відфільтрованими новинами
ENGLISH_NEWS_FILE = "news_en.json"  # Файл із новинами англійською
TRANSLATION_FILES = {
    "uk": "translations_uk.json",  # Файл із перекладеними новинами українською
    "de": "translations_de.json",  # Файл із перекладеними новинами німецькою
    "ru": "translations_ru.json"   # Файл із перекладеними новинами російською
}

def main():
    while True:
        print("\n--- Початок нового циклу ---")

        # 1. Збір і фільтрація новин
        print("🔍 Збір новин...")
        raw_news = parse_rss(RSS_FEED_URLS, KEYWORDS)  # Отримання новин із RSS-стрічок
        save_filtered_news(raw_news, RAW_NEWS_FILE)  # Збереження відфільтрованих новин у файл

        # 2. Обробка новин агентом OpenAI
        print("📝 Обробка новин...")
        process_news(RAW_NEWS_FILE, ENGLISH_NEWS_FILE)  # Генерація новин англійською

        # 3. Переклад новин
        print("🌍 Переклад новин...")
        translate_news(ENGLISH_NEWS_FILE, TRANSLATION_FILES)  # Переклад новин на кілька мов

        # 4. Публікація новин
        print("📢 Публікація новин...")
        for lang, file in TRANSLATION_FILES.items():
            publish_news(file, lang)  # Публікація новин для кожної мови

        # Очікування перед наступним циклом
        print(f"⏳ Очікування {CHECK_INTERVAL // 3600} годин до наступного циклу...")
        time.sleep(CHECK_INTERVAL)  # Затримка перед наступним запуском

if __name__ == "__main__":
    main()
