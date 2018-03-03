from lxml import html
import csv, os, json
import requests
from exceptions import ValueError
from time import sleep
import urlparse
import _thread

def AmazonParser(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url, headers=headers)
    while True:
        sleep(3)
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id, "saleprice")]/text()'
            XPATH_DEAL_PRICE = '//span[contains(@id,"dealprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABLITY = '//div[@id="availability"]//text()'

            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_DEAL_PRICE = doc.xpath(XPATH_DEAL_PRICE)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAW_AVAILABILITY = doc.xpath(XPATH_AVAILABLITY)

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            DEAL_PRICE = ' '.join(''.join(RAW_DEAL_PRICE).split()).strip() if RAW_DEAL_PRICE else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAW_AVAILABILITY).strip() if RAW_AVAILABILITY else None

            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            if page.status_code != 200:
                raise ValueError(str(page.status_code))

            data = {'name': NAME, 'deal_price': DEAL_PRICE, 'sale_price': SALE_PRICE, 'category': CATEGORY,
                    'original_price': ORIGINAL_PRICE, 'availability': AVAILABILITY, 'url': url}
            return data
        except Exception as e:
            print (e)


def ReadAsin(asin_id):
    url = "https://www.amazon.in/dp/" + asin_id
    return AmazonParser(url)


def parseIDfromURL(url):
    parse_url = urlparse.urlsplit(url)
    params = parse_url.path.split('/')
    for i in range(len(params)):
        if params[i] == "dp":
            return params[i + 1]
    return None


def substract(a, b):
    return "".join(a.rsplit(b))

def getASINPrices(idList):
    ids = idList.split(',')
    results = []
    jsonD={}
    for i in ids:
        results.append(ReadAsin(i))
    jsonD = json.dumps(results)