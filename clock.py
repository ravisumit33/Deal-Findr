from apscheduler.schedulers.blocking import BlockingScheduler
from deal_findr.cron import my_cron_job
import subprocess

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
	subprocess.call(('python manage.py my_cron_job'), shell=True, close_fds=True)
sched.start()
