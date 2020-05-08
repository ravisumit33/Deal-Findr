from deal_findr import models
from deal_findr.service import serviceStart, notifyDealStatus

def my_cron_job():
	deals = models.Deal.objects
	for deal in deals:
		customer = deal.customer
		created_at = deal.created_at
		if timezone.now() < created_at + datetime.timedelta(days=30):
			serviceStart(customer, deal)
		else:
			notifyDealStatus(customer, deal, False, price, productName)
			models.Deal.objects.filter(id=deal.id).delete()

