import logging
import requests

from email.mime.image import MIMEImage
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = logging.getLogger('testlogger')

def send_sms(mob_number, text):
    url = "https://www.fast2sms.com/dev/bulk"
    logger.info(mob_number)
    payload = "sender_id=FSTSMS&message=%s&language=english&route=p&numbers=%s" % (text, mob_number)
    headers = {
        'authorization': "mBUPKNinfGg2qVolyhFTQO14rd7CEYejzA3SpxXc6sI59tZDRuHVJqlFoeIZwS6fL0UC2XAa1cWk9PM7",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    logger.info(response.text)
    logger.info('SMS sent')

def send_email(email, subject, text, html):
    from_email, to = 'Deal Findr<ravisumit305@gmail.com>', email
    msg = EmailMultiAlternatives(subject, html, from_email, [to])
    msg.content_subtype = 'html'
    msg.mixed_subtype = 'related'
    img_path = staticfiles_storage.path('deal_findr/images/Gifts.gif')
    fp = open(img_path, 'rb')
    img = MIMEImage(fp.read())
    img.add_header('Content-ID', '<Gifts.gif>')
    msg.attach(img)
    msg.send()
    logger.info('Email sent')
 
