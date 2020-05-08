from . import models

def my_cron_job():
	deals = Deal.objects
	for deal in deals:
		customer = deal.customer
		#todo use created_at field
		serviceStart(customer, deal)

