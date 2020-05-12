import logging

from deal_findr import models
from deal_findr.service import serviceStart, notifyDealStatus

logger = logging.getLogger("testlogger")

def my_cron_job():
    logger.info("Starting cron job")
    deals = models.Deal.objects.all()
    num_deals = 0
    for deal in deals:
        customer = deal.customer
        serviceStart(customer, deal)
        num_deals += 1
    logger.info('Successfully monitored %d deals' % num_deals)
