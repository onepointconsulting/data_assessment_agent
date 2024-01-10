from datetime import datetime
import pytz


def generate_ISO_8601_timestamp():
    now_utc = datetime.now(pytz.utc)
    return now_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
