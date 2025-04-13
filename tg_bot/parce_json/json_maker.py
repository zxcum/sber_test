import re
import json


def parse_articles(text):
    pattern = r'Статья\s(\d{1,3}(?:\.\d)?)\s*(.*?)(?=\s*Статья\s\d|$)'
    articles = re.findall(pattern, text, re.DOTALL)
    result = {}
    for number, content in articles:
        result[number] = content[2:]
    return result



with open('output_cleaned.txt', 'r', encoding='utf-8') as file:
    text = file.read()
articles = parse_articles(text)
with open('articles_1.json', 'w', encoding='utf-8') as file:
    json.dump(articles, file, ensure_ascii=False, indent=4)

print(f"Найдено {len(articles)} статей. Результат сохранен в articles.json")