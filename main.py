import requests
import pprint as pp
import sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect('barilla_products.db')
cursor = conn.cursor()

locales = [
    # Americas
    'pt-BR',  # Brazil (Portuguese)
    'es-PR',  # Puerto Rico
    'en-CA',  # Canada (English)
    'fr-CA',  # Canada (Français)
    'en-US',  # English (Assuming United States)
    'es-LATAM',  # LATAM (Spanish) - Note: 'LATAM' is not a standard country code
    'es-MX',  # Mexico (Spanish)

    # Europe
    'de-DE',  # Deutsch (Assuming Germany)
    'bs-BA',  # BIH (Assuming Bosnia and Herzegovina, Bosnian language)
    'nl-BE',  # Belgium (Dutch)
    'fr-BE',  # Belgium (Français)
    'bg-BG',  # Bulgaria
    'hr-HR',  # Croatian
    'cs-CZ',  # Czech
    'da-DK',  # Danish
    'fr-FR',  # Français (Assuming France)
    'el-GR',  # Greek
    'hu-HU',  # Hungarian
    'it-IT',  # Italian
    'nl-NL',  # Dutch (Assuming Netherlands)
    'nb-NO',  # Norwegian (Bokmål)
    'pl-PL',  # Polish
    'pt-PT',  # Portuguese (Assuming Portugal)
    'ro-RO',  # Romanian
    'sr-RS',  # Serbian
    'sl-SI',  # Slovenian
    'es-ES',  # Spanish (Assuming Spain)
    'sv-SE',  # Swedish
    'fr-CH',  # Switzerland (Français)
    'de-CH',  # Switzerland (Deutsch)
    'tr-TR',  # Turkish

    # Africa, Asia, and Australia
    'en-AU',  # Australia
    'en-SG',  # Singapore
    'ar-SA',  # Arabic (Assuming Saudi Arabia)
    'ar-AE',  # Arabic (UAE)
    'he-IL',  # Hebrew (Assuming Israel)
    'ko-KR',  # South Korea
]


# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        title TEXT,
        cardImage TEXT,
        packShot TEXT,
        url TEXT
    )
''')

headers = {
    'Host': 'www.barilla.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Accept': '*/*',
    # 'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Alt-Used': 'www.barilla.com',
    'Connection': 'keep-alive',
    'Cookie': 'your-cookie-string-here',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'TE': 'trailers'
}

for locale in locales: 
    url = f'https://www.barilla.com/{locale}'

    resultpage = requests.get(url, headers=headers)

        # Check if the request was successful
    if resultpage.status_code != 200:
        data = "Failed to retrieve data for %s", locale

    html_content = resultpage.text

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the container div
    product_dropdown = soup.find('div', class_='megaDropdown--products')

    # Extract all the <a> elements with class 'categoryList-item'
    category_list_items = product_dropdown.find_all('a', class_='categoryList-item')

    # Now, extract the URLs
    urls = [item.get('href') for item in category_list_items]



    # Output the list of URLs
    for sub in urls:
        # pp.pprint(url)
        suburl = f'https://www.barilla.com{sub}'
        print(suburl)

    #     response = requests.get(url, headers=headers)

    #     print(response.text)

    #     soup = BeautifulSoup(response.text, 'html.parser')

    #     listofPastaForms = soup.find('form', class_='resultsForm')

    #     listofPasta = listofPastaForms.get('action')


    #     finalurl = f'https://www.barilla.com/{sub}'
        
    #     data = requests.get(finalurl).json()

    #     # # Output the data or the error message
    #     # pp.pprint(data)

    #     # Insert CSV data into the database
    #     for row in data['results']:
    #         cursor.execute('INSERT INTO products (title, cardImage, packShot, url) VALUES (?, ?, ?, ?)', (row['title'], row['packShot'], row['cardImage'], row['url']))

# Commit changes and close the connection
conn.commit()
conn.close()
