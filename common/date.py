from datetime import datetime


def get_date_now() -> "datetime":
    return datetime.utcnow()


def format_date(date_time: datetime) -> str:
    return date_time.strftime("%A %d %B %Y, %H:%M:%S")


def seconds_till_midnight():
    hour, minute, seconds = 23, 59, 59
    now = datetime.now()
    time = now.replace(hour=hour, minute=minute, second=seconds)
    return (time - now).seconds
