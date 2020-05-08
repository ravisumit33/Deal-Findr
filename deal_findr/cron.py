from deal_findr import models
from deal_findr.service import serviceStart, notifyDealStatus

def my_cron_job():
	deals = models.Deal.objects
	for deal in deals:
		customer = deal.customer
		serviceStart(customer, deal)

