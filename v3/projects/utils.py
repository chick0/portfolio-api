from datetime import datetime


def to_pretty(date: datetime) -> str:
    return date.strftime("%Y년 %m월 %d일")
