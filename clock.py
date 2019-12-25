from apscheduler.schedulers.blocking import BlockingScheduler

import mycalendar

scheduler = BlockingScheduler(time='Asia/Tokyo')

@scheduler.scheduled_job('cron', hour=18)
def scheduled_job():
    mycalendar.update_calendar()

scheduler.start()
