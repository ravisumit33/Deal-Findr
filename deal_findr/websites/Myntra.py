import bs4, requests
import logging

logger = logging.getLogger(__name__)

def list_name(list):
    if len(list) > 0:
        return list[0].get_text().strip()
    return ''

def list_price(list):
    if len(list) > 0:
        return float(list[0].get_text().strip().replace(',', '')[1:])
    return float('inf')


def getObject(productURL):
    getPage = requests.get(productURL, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
    })
    getPage.raise_for_status()

    item = bs4.BeautifulSoup(getPage.text, 'html.parser')
    return item
 
def getName(productURL):
    item = getObject(productURL)
    f = open("m.html", "w")
    f.write(item.prettify())
    item_name = item.find_all(class_="pdp-name")
    print(item_name)
    logger.info(str(item_name))
    return str(item_name)

def getPrice(productURL):
    item = getObject(productURL)
    price = item.find("div", class_= "pdp-price-info")
    logger.info(price)
    return price


productURL = "https://www.myntra.com/jeans/roadster/roadster-time-travlr-men-black-skinny-fit-mid-rise-clean-look-stretchable-jeans/2425786/buy"
print(getName(productURL))
print(getPrice(productURL))
