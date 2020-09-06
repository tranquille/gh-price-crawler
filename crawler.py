import logging
import argparse
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('--debug', default=False, type=bool)
args = parser.parse_args()
if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

urls = []
with open("urls.txt", "r") as urls_reader:
    urls = urls_reader.readlines()

for url in urls:
    if url.startswith('#'):
        continue

    logging.debug(f'Fetching url {url}')
    r = requests.get(url)
    logging.debug(f'Request status was: {r.status_code}')
    if r.status_code == requests.codes.ok:
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        #<h1 class="variant__header__headline" itemprop="name">
        title = soup.find('h1', class_='variant__header__headline')

        prices = soup.find_all('meta', itemprop='lowPrice')
        logging.debug(f'Found this lowPrice meta tags: {prices}')
        for price in prices:
            print(title.string, price['content'])
