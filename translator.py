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

# Функція для перекладу окремого тексту
def translate_text(text, target_language):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Translate the following text into {target_language}:"},
                {"role": "user", "content": text}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ Error translating text to {target_language}: {e}")
        return None

# Функція для перекладу всіх новин
def translate_news(input_file, output_files):
    if not os.path.exists(input_file):
        print(f"❌ Input file {input_file} not found.")
        return

    # Завантаження новин із файлу
    with open(input_file, "r", encoding="utf-8") as f:
        news_data = json.load(f)

    for lang, output_file in output_files.items():
        translated_news = []
        print(f"🔄 Translating news into {lang}...")

        for index, news_item in enumerate(news_data, start=1):
            print(f"   Translating item {index}/{len(news_data)}: {news_item['original']['title']}")
            translation = translate_text(news_item["processed"], lang)
            if translation:
                translated_news.append({
                    "original": news_item["original"],
                    "translation": translation
                })
            else:
                print(f"❌ Failed to translate item {index} into {lang}")

        # Збереження перекладів у файл
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(translated_news, f, ensure_ascii=False, indent=4)

        print(f"✅ Translations for {lang} saved to {output_file}")

if __name__ == "__main__":
    TRANSLATION_FILES = {
        "uk": "translations_uk.json",
        "de": "translations_de.json",
        "ru": "translations_ru.json"
    }
    translate_news("news_en.json", TRANSLATION_FILES)
