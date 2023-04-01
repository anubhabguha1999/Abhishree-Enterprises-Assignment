import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
from datetime import datetime

url = "https://www.theverge.com/"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

articles = soup.find_all('article')

data = []

for article in articles:
    link = article.find('a')['href']
    
    headline = article.find('h2').text.strip()
    
    author = article.find('span', {'class': 'c-byline__item'}).text.strip()
    
    date = article.find('time')['datetime']
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d-%m-%Y')
    
    data.append((link, headline, author, date))

filename = datetime.now().strftime('%d%m%Y') + '_verge.csv'
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'URL', 'headline', 'author', 'date'])
    for i, item in enumerate(data):
        writer.writerow([i+1, item[0], item[1], item[2], item[3]])

conn = sqlite3.connect('articles.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS articles
             (id INTEGER PRIMARY KEY,
              url TEXT,
              headline TEXT,
              author TEXT,
              date TEXT)''')

for item in data:
    c.execute("INSERT INTO articles (url, headline, author, date) VALUES (?, ?, ?, ?)", item)

conn.commit()
conn.close()
