from deal_findr import models
from deal_findr.service import serviceStart

def my_cron_job():
	deals = models.Deal.objects
	for deal in deals:
		customer = deal.customer
		#todo use created_at field
		serviceStart(customer, deal)

