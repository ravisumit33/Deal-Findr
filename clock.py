from apscheduler.schedulers.blocking import BlockingScheduler
from deal_findr.cron import my_cron_job

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')
    my_cron_job()

sched.start()