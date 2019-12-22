from apscheduler.schedulers.blocking import BlockingScheduler

import calendar

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=18)
def scheduled_job():
    calendar.update_calendar()

sched.start()
