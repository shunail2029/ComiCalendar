from apscheduler.schedulers.blocking import BlockingScheduler

import mycalendar

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=18)
def scheduled_job():
    mycalendar.update_calendar()

sched.start()
