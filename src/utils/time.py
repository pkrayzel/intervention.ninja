from datetime import datetime
import time

MILLISECONDS_PER_SECOND = 1000
MILLISECONDS_PER_MINUTE = 60 * 1000


def get_timestamp_from_date(date):
    return int(time.mktime(date.timetuple())) * MILLISECONDS_PER_SECOND


def get_current_timestamp():
    return get_timestamp_from_date(datetime.now())


def get_timestamp_minute_ago():
    return get_current_timestamp() - MILLISECONDS_PER_MINUTE
