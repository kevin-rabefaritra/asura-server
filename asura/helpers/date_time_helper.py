from django.utils import timezone
from datetime import date

def now():
    """
    Returns the current time (UTC)
    :return:
    """
    return timezone.now()


def to_date(date_str: str) -> date or None:
    """
    Converts a date str to a date instance
    Returns None of the date format is not valid
    :param date_str must be in ISO format YYYY-MM-DD
    """
    try:
        return date.fromisoformat(date_str)
    except Exception as e:
        return None

def date_to_string(value) -> str:
    """
    Converts a date to a ISO format string
    """
    return value.strftime("%Y/%m/%d")
