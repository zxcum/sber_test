import sqlite3
import json
import pandas as pd

conn = sqlite3.connect('tk.db')


cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY,
    number TEXT,
    article_text TEXT
)
''')
with open('articles_1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    articles = data

print(articles)
for article in articles.keys():
    cursor.execute("INSERT INTO articles (number, article_text) VALUES (?, ?)",
                   (str(article), str(articles[article])))


print(pd.read_sql("SELECT * FROM articles", conn))
conn.commit()
conn.close()