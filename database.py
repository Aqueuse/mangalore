import sys

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


client = MongoClient('mongodb://localhost:27017/')
db = client["multipass"]

try:
    client = MongoClient('localhost', 27017)
except ConnectionFailure:
    print("connection failed")
    sys.exit(1)


def get_token(social_network):
    print("reload the token for the social_network in the database")
    print("return them")


# ---------------- tasks -------------------- #

def get_today_monthly_tasks(current_date, current_day_int, current_month):
    monthly_result = db["users"].find({
        '$or': [
            {
                'facebook.date': {'$lte': current_date, '$regex': current_day_int+'T'},
                'facebook.repetition.months': {'$regex': current_month},
                'facebook.repetition.frequency': {'$regex': 'monthly'}
            },
            {
                'twitter.date': {'$lte': current_date},
                'twitter.repetition.months': {'$regex': current_month},
                'twitter.repetition.frequency': {'$regex': 'monthly'}
            },
            {
                'instagram.date': {'$lte': current_date},
                'instagram.repetition.months': {'$regex': current_month},
                'instagram.repetition.frequency': {'$regex': 'monthly'}
            }
        ]},
        {'_id': 0}
    )
    return list(monthly_result)


def get_today_weekly_tasks(current_date, current_day):
    weekly_result = db["users"].find({
        '$or': [
            {
                'facebook.date': {'$lte':  current_date},
                'facebook.repetition.days': {'$regex': current_day},
                'facebook.repetition.frequency': {'$regex': 'weekly'},
            },
            {
                'twitter.date': {'$lte': current_date},
                'twitter.repetition.days': {'$regex': current_day},
                'twitter.repetition.frequency': {'$regex': 'weekly'},
            },
            {
                'instagram.date': {'$lte': current_date},
                'instagram.repetition.days': {'$regex': current_day},
                'instagram.repetition.frequency': {'$regex': 'weekly'},
            }
        ]},
        {'_id': 0}
    )
    return list(weekly_result)


def get_today_custom_tasks(current_date, current_day, current_month):
    custom_result = db["users"].find({
        '$or': [
            {
                'facebook.date': {'$lte':  current_date},
                'facebook.repetition.days': {'$regex': current_day},
                'facebook.repetition.months': {'$regex': current_month},
                'facebook.repetition.frequency': {'$regex': 'custom'},
            },
            {
                'twitter.date': {'$lte': current_date},
                'twitter.repetition.days': {'$regex': current_day},
                'twitter.repetition.months': {'$regex': current_month},
                'twitter.repetition.frequency': {'$regex': 'custom'},
            },
            {
                'instagram.date': {'$lte': current_date},
                'instagram.repetition.days': {'$regex': current_day},
                'instagram.repetition.months': {'$regex': current_month},
                'instagram.repetition.frequency': {'$regex': 'custom'},
            }
        ]},
        {'_id': 0}
    )
    return list(custom_result)


# ---------------- helpers -------------------- #

def get_max_taskid(social_network_tasks):
    ids = []
    for element in social_network_tasks:
        ids.append(int(element["id"]))
    ids.sort()
    if len(ids) == 0:
        return 0
    if len(ids) > 0:
        ids.sort()
        ids.reverse()
        max_id = ids[0]
        return max_id


def set_id():
    result = list(db["users"].find({}, {'id': 1, '_id': 0}).distinct("id"))
    return get_max_taskid(result) + 1


def get_item_with_int_id(item):
    item['id'] = int(item['id'])
    return item


def get_item_by_filter(json_filter):
    raw_result = db["users"].find_one(json_filter, {'_id': 0})
    if raw_result is None:
        return None
    else:
        return raw_result
