from requests_html import AsyncHTMLSession
import pyppdf.patch_pyppeteer
from pyppeteer import launch

class WebUtility():

    def __init__(self):
        self.asession = AsyncHTMLSession()
        self.browser = None

    async def getObject(self, productURL):
        if self.browser is None:
            self.browser = await launch({
                'ignoreHTTPSErrors': True,
                'headless': True,
                'handleSIGINT': False,
                'handleSIGTERM': False,
                'handleSIGHUP': False,
                'args': [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3312.0 Safari/537.36"'
                ]
            })
            self.asession._browser = self.browser
        resp = await self.asession.get(productURL)
        resp.raise_for_status()
        await resp.html.arender(timeout=0)
        return resp.html
     
    def format_name(self, content):
        return content.text.strip()
 
