from requests_html import AsyncHTMLSession
import pyppeteer

class WebUtility():

    def __init__(self):
        self.asession = AsyncHTMLSession()
        self.browser = None

    async def getObject(self, productURL):
        if self.browser is None:
            self.browser = await pyppeteer.launch({
                'ignoreHTTPSErrors': True,
                'headless': True,
                'handleSIGINT': False,
                'handleSIGTERM': False,
                'handleSIGHUP': False,
                'args': [
                    '--no-sandbox',
                    '--disable-setuid-sandbox'
                ]
            })
            self.asession._browser = self.browser
        resp = await self.asession.get(productURL)
        await resp.html.arender()
        return resp.html
     
    def format_name(self, content):
        return content.text.strip()
 
