import datetime


def generate_report_date() -> str:
    report_date = datetime.datetime.now()
    return report_date.strftime("%a, %d %b %Y")
