import requests
import sqlite3
import csv
from bs4 import BeautifulSoup
import pprint as pp

# Database connection
conn = sqlite3.connect('barilla_prod.db')
cursor = conn.cursor()

# Create or ensure the existence of the products table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        title TEXT,
        cardImage TEXT,
        packShot TEXT,
        url TEXT,
        guid TEXT
    )
''')

# Common headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

# Add the 'Cookie' header with your browser's cookies
cookies = {
    'AppGwAffinity-CDCORS': 'accd7f58b179e9189dbda9eb8881fa70',
    'AppGwAffinity-CD': 'accd7f58b179e9189dbda9eb8881fa70',
    'website_brazil_pt_br#lang': 'pt-BR',
    'ASP.NET_SessionId': 'nu2hwaef053z42a4e4czx4j0',
    '__cf_bm': 'YpAHOM5pnnWJqR0szS4hawHMwo917ynjREjQII0NXGI-1706704332-1-AdnvGM88AFO36FfrAQvEZuwu+VoB9hfABuWAL8vG4WuW1SBWthxuXebiEMD1toyEw3BL7A/8f/lAni2vvItpZWY=',
}

# Open the CSV file and read data
with open('subpasta.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)

    # Insert CSV data into the database
    for row in csvreader:
        # print("Sending request for ", row[0])

        # Send the request with cookies
        response = requests.get(f'https://www.barilla.com{row[0]}', headers=headers, cookies=cookies)
        if response.status_code == 200:
            
            data = response.json()

            # # # Output the data or the error message
            # pp.pprint(data)

            if data['results'] is None:
                print("Failed to access ", f'https://www.barilla.com{row[0]}')

            else:
                # Insert CSV data into the database
                for row in data['results']:
                    cursor.execute('INSERT INTO products (title, cardImage, packShot, url, guid) VALUES (?, ?, ?, ?, ?)', (row['title'], row['packShot'], row['cardImage'], row['url'], row['guid']))

            

# Commit changes and close the connection
conn.commit()
conn.close()
