import logging

logger = logging.getLogger(__name__)

class Myntra():
 
    def __init__(self):
        self.page = None

    def format_price(self, content):
        return float(content.text.strip()[3:].replace(',', ''))

    async def getName(self, productURL, web_util):
        if self.page is None:
            self.page = await web_util.getObject(productURL)
        item_name = web_util.format_name(self.page.find(".pdp-name")[0])
        return item_name

    async def getPrice(self, productURL, web_util):
        if self.page is None:
            self.page = await web_util.getObject(productURL)
        item_price = self.format_price(self.page.find(".pdp-price")[0])
        return item_price
