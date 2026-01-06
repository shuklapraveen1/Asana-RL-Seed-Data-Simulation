import random
from datetime import datetime, timedelta


def get_now() -> datetime:
    """
    Returns the current UTC datetime.
    """
    return datetime.utcnow()


def random_past_datetime(months_back: int) -> datetime:
    """
    Returns a random datetime within the past `months_back` months.
    """
    now = get_now()
    days_back = months_back * 30
    random_days = random.randint(0, days_back)
    random_seconds = random.randint(0, 86400)

    return now - timedelta(days=random_days, seconds=random_seconds)


def is_weekend(date: datetime) -> bool:
    """
    Checks if a given date falls on a weekend.
    """
    return date.weekday() >= 5


def next_weekday(date: datetime) -> datetime:
    """
    If date falls on a weekend, move it to the next Monday.
    """
    while is_weekend(date):
        date += timedelta(days=1)
    return date


def random_due_date(created_at: datetime) -> datetime | None:
    """
    Generates a realistic due date based on task creation time.

    Distribution:
    - ~10% no due date
    - ~25% within 7 days
    - ~40% within 30 days
    - ~20% within 1–3 months
    - ~5% overdue
    """
    roll = random.random()

    if roll < 0.10:
        return None

    if roll < 0.35:
        due = created_at + timedelta(days=random.randint(1, 7))
    elif roll < 0.75:
        due = created_at + timedelta(days=random.randint(8, 30))
    elif roll < 0.95:
        due = created_at + timedelta(days=random.randint(31, 90))
    else:
        due = created_at - timedelta(days=random.randint(1, 14))

    return next_weekday(due)


def completion_datetime(created_at: datetime) -> datetime:
    """
    Generates a realistic completion timestamp after task creation.
    """
    delay_days = random.randint(1, 14)
    completed_at = created_at + timedelta(days=delay_days)

    return completed_at
