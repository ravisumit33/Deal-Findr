import datetime, logging
import asyncio
import importlib
from channels.db import database_sync_to_async

from django.utils import timezone
from django.template import loader

from .notification import send_sms, send_email
from websites.Base import WebUtility
from deal_findr import models

logger = logging.getLogger("testlogger")

base_text_pos = "\nHi %s,\nWe have found your deal.\nThings are in your budget now :)\nYou can buy your product in Rs.%d.\n\nThank you for using Deal Findr"
base_text_neg = 'Hi %s,\n\nWe could not find your deal :(\nPrice of your product is still Rs.%d.\n\nThank you for using Deal Findr.'
base_subject_pos = 'Go ahead and buy on %s!'
base_subject_neg = 'Deal not found on %s'


def notifyDealStatus(customer, deal, deal_found, price):
    context = {
        'name' : customer.first_name, 
        'price' : int(price),
        'productURL' : deal.productURL,
        'productName' : deal.productName,
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
    logger.info(deal.budget)

    website_module = importlib.import_module('websites.' + deal.website)
    website_class = getattr(website_module, deal.website)
    website = website_class()

    web_util = WebUtility()

    try_count = 0

    if deal.productName == '': 
        while try_count < 5:
            try:
                productName = await website.getName(deal.productURL, web_util)
                obj = await database_sync_to_async(models.Deal.objects.filter)(id=deal.id)
                await database_sync_to_async(obj.update)(productName=productName)
                break
            except Exception as e:
                logger.error(str(e))
                try_count += 1
                await asyncio.sleep(1*60)

    if try_count == 5:
        logger.error("Unable to get product name")
        notifyError(customer, deal)
        obj = await database_sync_to_async(models.Deal.objects.filter)(id=deal.id)
        await database_sync_to_async(obj.delete)()
        return

    logger.info(deal.productName)

    logger.info("Price monitoring started...")
    price = float('inf')

    deal_done = False

    try:
        price = await website.getPrice(deal.productURL, web_util) 
        logger.info(str(price))
        if price <= deal.budget:
            deal_done = True
    except Exception as e:
        logger.error(str(e))
        pass

    if web_util.browser is not None:
        await web_util.browser.close()
        web_util.browser = None
    else:
        logger.error("Browser instance should not be None")

    if deal_done:
        notifyDealStatus(customer, deal, True, price)
        obj = await database_sync_to_async(models.Deal.objects.filter)(id=deal.id)
        await database_sync_to_async(obj.delete)()
    
    if(timezone.now() > deal.created_at + datetime.timedelta(days=30)):
        notifyDealStatus(customer, deal, False, price)
        obj = await database_sync_to_async(models.Deal.objects.filter)(id=deal.id)
        await database_sync_to_async(obj.delete)()
        logger.info("Deal expired")

    logger.info("Exiting Customer Service")


def serviceStart(customer, deal):
    asyncio.run(servCustomer(customer, deal))

