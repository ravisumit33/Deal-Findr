import bs4, requests
import logging

logger = logging.getLogger(__name__)


def getObject(productURL):
    getPage = requests.get(productURL, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
    })
    getPage.raise_for_status()

    item = bs4.BeautifulSoup(getPage.text, 'html.parser')
    return item
 
def getName(productURL):
    item = getObject(productURL)
    item_name = item.find(itemprop='name').get_text().strip()
    logger.info(str(item_name))
    return str(item_name)

def getPrice(productURL):
    item = getObject(productURL)
    price = float(item.find(itemprop='price').get_text().strip().replace(',', ''))
    logger.info(price)
    return price

