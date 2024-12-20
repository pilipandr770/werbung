import openai
import os
import json
from dotenv import load_dotenv

# Завантаження змінних із .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the .env file")

openai.api_key = OPENAI_API_KEY

# Функція для обробки новин
def process_news(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"❌ Input file {input_file} not found.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        raw_news = json.load(f)

    processed_news = []
    
    for index, news_item in enumerate(raw_news):
        try:
            print(f"🔄 Processing item {index + 1}/{len(raw_news)}: {news_item['title']}")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Використовуйте доступну модель
                messages=[
                    {"role": "system", "content": "You are an assistant that summarizes news articles."},
                    {"role": "user", "content": f"Title: {news_item['title']}\nSummary: {news_item['summary']}"}
                ]
            )
            processed_text = response['choices'][0]['message']['content']
            processed_news.append({"original": news_item, "processed": processed_text})
        except Exception as e:
            print(f"❌ Error processing news item {index + 1}: {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(processed_news, f, ensure_ascii=False, indent=4)

    print(f"✅ Processed {len(processed_news)} news items. Saved to {output_file}")

if __name__ == "__main__":
    process_news("filtered_data.json", "news_en.json")