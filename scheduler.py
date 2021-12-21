import datetime
import time
import schedule

import database
import socialNetworks
from socialNetworks import facebook, twitter, instagram

current_monthly_tasks = []
current_weekly_tasks = []
current_custom_tasks = []

date = datetime.date.today()
email = "jaimaille@gmail.com"


# ---------------- schedule -------------------- #

def do_schedule():
    schedule.every(10).seconds.do(check_tasks)
    while True:
        schedule.run_pending()
        time.sleep(1)


def check_tasks():
    global current_monthly_tasks
    global current_weekly_tasks
    global current_custom_tasks
    global date

    current_date = datetime.date.today()
    if date != current_date:
        date = current_date

        current_monthly_tasks = database.get_today_monthly_tasks(
            get_current_dateISOformat(),
            get_current_day_int(),
            get_current_month_string()
        )

        current_weekly_tasks = database.get_today_weekly_tasks(
            get_current_dateISOformat(),
            get_current_weekday_string()
        )

        current_custom_tasks = database.get_today_custom_tasks(
            get_current_dateISOformat(),
            get_current_weekday_string(),
            get_current_month_string()
        )

    do_tasks()


def do_tasks():
    global current_monthly_tasks
    global current_weekly_tasks

    for task in current_monthly_tasks:
        for facebook_task in task["facebook"]:
            socialNetworks.facebook.share_to_fb(facebook_task)
        for twitter_task in task["twitter"]:
            socialNetworks.twitter.share_to_twitter(twitter_task)
        for instagram_task in task["instagram"]:
            socialNetworks.instagram.share_to_instagram(instagram_task)

    for task in current_monthly_tasks:
        for facebook_task in task["facebook"]:
            socialNetworks.facebook.share_to_fb(facebook_task)
        for twitter_task in task["twitter"]:
            socialNetworks.twitter.share_to_twitter(twitter_task)
        for instagram_task in task["instagram"]:
            socialNetworks.instagram.share_to_instagram(instagram_task)

    for task in current_monthly_tasks:
        for facebook_task in task["facebook"]:
            socialNetworks.facebook.share_to_fb(facebook_task)
        for twitter_task in task["twitter"]:
            socialNetworks.twitter.share_to_twitter(twitter_task)
        for instagram_task in task["instagram"]:
            socialNetworks.instagram.share_to_instagram(instagram_task)


# ---------------- helpers -------------------- #


def get_current_weekday_string():
    days = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
    return days[datetime.date.today().weekday()]


def get_current_month_string():
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    return months[datetime.date.today().month-1]


def get_current_dateISOformat():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')


def get_current_day_int():
    return datetime.datetime.now().strftime('%d')
