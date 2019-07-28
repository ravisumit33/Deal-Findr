import datetime, logging
import os, sys, importlib
import bs4
from urllib.request import urlopen

from django.utils import timezone
from django.template import loader

from .notification import send_sms, send_email

dir_path = os.path.dirname(os.path.realpath(__file__))
websites_path = os.path.join(dir_path, 'websites')
sys.path.insert(0, websites_path)

logger = logging.getLogger(__name__)

base_text_pos = "\nHi %s,\nWe have found your deal.\nThings are in your budget now :)\nYou can buy your product in Rs.%d.\n\nThank you for using Deal_Findr"
base_text_neg = 'Hi %s,\n\nWe could not find your deal :(\nPrice of your product is still Rs.%d.\n\nThank you for using Deal_Findr.'
base_subject_pos = 'Go ahead and buy on %s!'
base_subject_neg = 'Deal not found on %s'


def serv_customer(first_name, mobNumber, email, website, budget, productURL):
    logger.info("Starting Customer Service")
    price = float('inf')
    logger.info(website)
    website_module = importlib.import_module(website)
    productName = website_module.getName(productURL)
    logger.info(productName)
    deadline = timezone.now() + datetime.timedelta(days=30)
    logger.info("Price monitoring started...")
    while timezone.now() < deadline and  price > budget:
        price = website_module.getPrice(productURL) 
        logger.info(str(price))
    if(timezone.now() < deadline):
        context = {
            'name' : first_name, 
            'price' : int(price),
            'productURL' : productURL,
            'productName' : productName,
            'img_name' : 'Gifts.gif',
        }
        html = loader.render_to_string('deal_findr/email_pos.html', context)
        text = base_text_pos % (first_name, price)
        subject = base_subject_pos % website
        #send_sms(mobNumber, text)
        send_email(email, subject, text, html)
    else:
        text = base_text_neg % (first_name, price)
        subject = base_subject_neg % (website)
        context = {
            'name' : first_name, 
            'price' : price,
            'productURL' : productURL,
            'productName' : productName,
            'formURL' : '#' 
        }
        html = loader.render_to_string('deal_findr/email_neg.html', context)
        send_sms(mobNumber, text)
        send_email(email, subject, text, html)
    
    logger.info("Exiting Customer Service")



