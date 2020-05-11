from apscheduler.schedulers.blocking import BlockingScheduler
from deal_findr.cron import my_cron_job

def clock_fun():
	sched = BlockingScheduler()
	@sched.scheduled_job('interval', minutes=5)
	def timed_job():
		my_cron_job()
	sched.start()
