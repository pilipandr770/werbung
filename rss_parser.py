import feedparser
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

# Функція для очищення HTML-тегів
def clean_html(text):
    return BeautifulSoup(text, "html.parser").get_text()

# Функція для перевірки ключових слів у тексті
def contains_keywords(text, keywords):
    return any(keyword.lower() in text.lower() for keyword in keywords)

# Функція для парсингу RSS
def parse_rss(feed_urls, keywords):
    all_news = []
    for url in feed_urls:
        print(f"🔍 Парсимо: {url}")
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.get("title", "").strip()
                summary = clean_html(entry.get("summary", "")).strip()
                link = entry.get("link", "").strip()
                published = entry.get("published", None)
                if not published:
                    published = datetime.now().isoformat()

                if contains_keywords(title, keywords) or contains_keywords(summary, keywords):
                    news_item = {
                        "title": title,
                        "summary": summary,
                        "link": link,
                        "published": published
                    }
                    all_news.append(news_item)
        except Exception as e:
            print(f"❌ Помилка під час парсингу {url}: {e}")
    return all_news

# Функція для збереження новин у JSON-файл
def save_filtered_news(news, output_file):
    if not news:
        print("⚠️ Немає нових новин для збереження.")
        return
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=4)
    print(f"✅ Новини збережено у {output_file} (всього: {len(news)})")

if __name__ == "__main__":
    TEST_FEEDS = [
        "https://openai.com/blog/rss",
        "https://ai.googleblog.com/feeds/posts/default"
    ]
    TEST_KEYWORDS = ["AI", "machine learning", "deep learning"]
    print("--- Початок парсингу RSS ---")
    news = parse_rss(TEST_FEEDS, TEST_KEYWORDS)
    save_filtered_news(news, "test_filtered_data.json")
    print("--- Завершено ---")
