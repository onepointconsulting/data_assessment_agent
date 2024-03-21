from datetime import datetime
import pytz


def generate_ISO_8601_timestamp():
    now_utc = datetime.now(pytz.utc)
    return now_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def generate_footer_date():
    now = datetime.now()
    return now.strftime("%d %b %Y")


if __name__ == "__main__":
    print(generate_footer_date())
