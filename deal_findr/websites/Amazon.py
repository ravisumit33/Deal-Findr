import logging

logger = logging.getLogger(__name__)

class Amazon():

    def __init__(self):
        self.page = None
 
    def format_price(self, content):
        return float(content.text.strip()[2:].replace(',', ''))

    async def getName(self, productURL, web_util):
        if self.page is None:
            self.page = await web_util.getObject(productURL)
        item_name = WebUtility.format_name(self.page.find('#productTitle')[0])
        return item_name

    async def getPrice(self, productURL, web_util):
        if self.page is None:
            self.page = await web_util.getObject(productURL)
        regular_price = self.format_price(self.page.find('#priceblock_ourprice')[0])
        deal_price = self.format_price(self.page.find('#priceblock_dealprice')[0])
        return min(regular_price, deal_price)

