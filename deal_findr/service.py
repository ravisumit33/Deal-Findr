import datetime, logging
import asyncio
import os, importlib
import bs4
from urllib.request import urlopen

from django.utils import timezone
from django.template import loader

from .notification import send_sms, send_email

logger = logging.getLogger(__name__)

base_text_pos = "\nHi %s,\nWe have found your deal.\nThings are in your budget now :)\nYou can buy your product in Rs.%d.\n\nThank you for using Deal_Findr"
base_text_neg = 'Hi %s,\n\nWe could not find your deal :(\nPrice of your product is still Rs.%d.\n\nThank you for using Deal_Findr.'
base_subject_pos = 'Go ahead and buy on %s!'
base_subject_neg = 'Deal not found on %s'


async def servCustomer(customer, deal):
    logger.info("Starting Customer Service")
    logger.info(deal.website)

    website_module = importlib.import_module('websites.' + deal.website)
    website_class = getattr(website_module, deal.website)
    website = website_class()
    from websites.Base import WebUtility

    web_util = WebUtility()
    productName = await website.getName(deal.productURL, web_util)
    logger.info(productName)

    deadline = timezone.now() + datetime.timedelta(days=30)
    logger.info("Price monitoring started...")
    price = float('inf')
    while timezone.now() < deadline and  price > deal.budget:
        price = await website.getPrice(deal.productURL, web_util) 
        logger.info(str(price))

    await web_util.browser.close()
    web_util.browser = None

    if(timezone.now() < deadline):
        context = {
            'name' : customer.first_name, 
            'price' : int(price),
            'productURL' : deal.productURL,
            'productName' : productName,
            'img_name' : 'Gifts.gif',
        }
        html = loader.render_to_string('deal_findr/email_pos.html', context)
        text = base_text_pos % (customer.first_name, price)
        subject = base_subject_pos % deal.website
        #send_sms(customer.phone, text)
        send_email(customer.email, subject, text, html)
    else:
        text = base_text_neg % (customer.first_name, price)
        subject = base_subject_neg % (deal.website)
        context = {
            'name' : customer.first_name, 
            'price' : price,
            'productURL' : deal.productURL,
            'productName' : productName,
            'formURL' : '#' 
        }
        html = loader.render_to_string('deal_findr/email_neg.html', context)
        send_sms(customer.phone, text)
        send_email(customer.email, subject, text, html)
    
    logger.info("Exiting Customer Service")


def serviceStart(customer, deal):
    asyncio.run(servCustomer(customer, deal))

