"""
Scrape brand websites every set interval for updated apparel catalogue.
"""
# Imporing Libraries
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import time, json, pathlib

# Initializing Session
session = HTMLSession()

# Scraping interval - 1 hour
interval = 3600

# Load news sources from a JSON file
sources_path = pathlib.Path(__file__).with_name('sources.json')
with sources_path.open('r') as f:
    sources = json.load(f)

# OLD NAVY
for source in sources:
    # Getting product urls
    main_session = session.get(source['site_url'])
    soup = BeautifulSoup(main_session.content, features="xml")
    product_urls = soup.find_all("loc")
    # Extracting product details
    for product_url in product_urls:
        try:
            # Initializing product session
            product_session = session.get(product_url.text)
            product_soup = BeautifulSoup(product_session.content, "html.parser")
            # Getting product title
            product_title = product_soup.find("h1", source['titleClass']).text
            # Getting product price
            product_price = product_soup.find("span", source['priceClass']).text
            # Getting product link
            product_link = product_url.text
            # Getting product images
            product_image_tags = product_soup.find("div", source['ImageClass']).find_all('img')
            product_images = []
            # Getting product image urls
            for image in product_image_tags:
                product_images.append(source['ImageUrl']+image['src'])
            # Printing product details
            print(f'Title: {product_title}\nPrice: {product_price}\nLink: {product_link}\nImages: {product_images}\n-----')
        except Exception as e:
            print(e)
        # Sleep of 1 second
        time.sleep(1)