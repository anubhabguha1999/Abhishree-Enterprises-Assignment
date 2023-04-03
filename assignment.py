import requests
from bs4 import BeautifulSoup
import csv
import sqlite3


# Install the packages
# pip install requests
# pip install bs4
# pip install csv
# pip install beautifulsoap4

#Setting The URL
targeturl = "https://www.theverge.com/"

#connecting with the SQL database 
connection = sqlite3.connect('sqldatabase.db')
cursor = connection.cursor()

#Generating Request
res = requests.get(targeturl)
html = res.content

s = BeautifulSoup(html, "html.parser")

# for TITLE
findtitle = s.find_all('a', class_='group-hover:shadow-underline-franklin')

# for URLs
findurls = s.find_all('a', class_='block h-full w-full')

# for DATE
finddates = s.find_all('span', class_='text-gray-63 dark:text-gray-94')

# for AUTHOR
findauthor = s.find_all(
    'a', class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8')


titles = []
authors = []
dates = []
urls = []


# Appending the values of DATE
for date in finddates:
    date = date.text
    dates.append(date)

# Appending the values of TITLE
for title in findtitle:
    title = title.text
    titles.append(title)

# Appending the values of URLs
for urlappend in findurls:
    url = targeturl + urlappend['href']
    urls.append(url)

# Appending the values of AUTHOR
for author in findauthor:
    author = author.text
    authors.append(author)


#Creating the CSV or Excel File
filename = "ExcelFile.csv"

#Writing the file and Appending the Values
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['title', 'url', 'author', 'date'])
    for i in range(len(titles)):
        writer.writerow([titles[i], urls[i], authors[i], dates[i]])

# query for SQL 
cursor.execute('''CREATE TABLE IF NOT EXISTS my_table
                (id INTEGER PRIMARY KEY, title TEXT, url TEXT, author TEXT, date TEXT)''')


for i in range(len(titles)):
    title = titles[i]
    url = urls[i]
    author = authors[i]
    date = dates[i]

#Inserting the values of title, url, author and date in SQL
    cursor.execute(
        "SELECT * FROM my_table WHERE title = ? AND url = ? AND author = ? AND date = ?", (title, url, author, date))
    result = cursor.fetchone()
    if not result:
        cursor.execute(
            "INSERT INTO my_table (title, url, author, date) VALUES (?, ?, ?, ?)", (title, url, author, date))

# commiting the connection
connection.commit()
#closing the connection
connection.close()
