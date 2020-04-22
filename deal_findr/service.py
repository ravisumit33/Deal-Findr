import datetime, logging
import asyncio
import importlib

from django.utils import timezone
from django.template import loader

from .notification import send_sms, send_email
from websites.Base import WebUtility

logger = logging.getLogger("testlogger")

base_text_pos = "\nHi %s,\nWe have found your deal.\nThings are in your budget now :)\nYou can buy your product in Rs.%d.\n\nThank you for using Deal_Findr"
base_text_neg = 'Hi %s,\n\nWe could not find your deal :(\nPrice of your product is still Rs.%d.\n\nThank you for using Deal_Findr.'
base_subject_pos = 'Go ahead and buy on %s!'
base_subject_neg = 'Deal not found on %s'


def notifyDealStatus(customer, deal, deal_found, price, productName):
    context = {
        'name' : customer.first_name, 
        'price' : int(price),
        'productURL' : deal.productURL,
        'productName' : productName,
        'img_name' : 'Gifts.gif',
    }
    if deal_found:
        context['img_name'] = 'Gifts.gif'
        email_template = 'email_pos.html'
        text_template = base_text_pos
        subject_template = base_subject_pos
    else:
        context['formURL'] = '#'
        email_template = 'email_neg.html'
        text_template = base_text_neg
        subject_template = base_subject_neg

    html = loader.render_to_string('deal_findr/' + email_template, context)
    text = text_template % (customer.first_name, price)
    subject = subject_template % deal.website
    #send_sms(customer.phone, text)
    send_email(customer.email, subject, text, html)

def notifyError(customer, deal):
    logger.info("Error notified")
    pass

async def servCustomer(customer, deal):
    logger.info("Starting Customer Service")
    logger.info(deal.website)

    website_module = importlib.import_module('websites.' + deal.website)
    website_class = getattr(website_module, deal.website)
    website = website_class()

    web_util = WebUtility()

    try_count = 0
    while try_count < 10:
        try:
            productName = await website.getName(deal.productURL, web_util)
            break
        except:
           try_count += 1
           await asyncio.sleep(5*60)

    if try_count == 10:
        logger.error("Unable to get product name")
        notifyError(customer, deal)
        return

    logger.info(productName)

    deadline = timezone.now() + datetime.timedelta(days=30)
    logger.info("Price monitoring started...")
    price = float('inf')
    while timezone.now() < deadline:
        try:
            price = await website.getPrice(deal.productURL, web_util) 
            logger.info(str(price))
            if price <= deal.budget:
                break
        except:
            pass
        await asyncio.sleep(5*60)

    await web_util.browser.close()
    web_util.browser = None

    if price == float('inf'):
        logger.error("Unable to get product error")
        notifyError(customer, deal)
        return
    
    if(timezone.now() < deadline):
        notifyDealStatus(customer, deal, True, price, productName)
    else:
        notifyDealStatus(customer, deal, False, price, productName)

    logger.info("Exiting Customer Service")


def serviceStart(customer, deal):
    asyncio.run(servCustomer(customer, deal))

