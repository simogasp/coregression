import datetime
from typing import Union, Iterable as typeIterable
from collections.abc import Iterable


def day_of_year_to_date(day: Union[int, float, typeIterable], year=None) -> Union[
    datetime.datetime, typeIterable[datetime.datetime]]:
    if year is None:
        year = datetime.datetime.now().year

    if isinstance(day, Iterable):
        return list(day_of_year_to_date(d) for d in day)
    else:
        return datetime.datetime(int(year), 1, 1) + datetime.timedelta(days=int(day))


def date_to_string(date: Union[datetime.datetime, typeIterable[datetime.datetime]], date_format: str = '%d %b'):
    if isinstance(date, Iterable):
        return list(date_to_string(d, date_format) for d in date)
    else:
        return date.strftime(date_format)


def day_of_year_to_string(day: Union[int, float, typeIterable], date_format: str = '%d %b') -> Union[
    str, typeIterable[str]]:
    if isinstance(day, Iterable):
        return list(day_of_year_to_string(d, date_format) for d in day)
    else:
        return date_to_string(day_of_year_to_date(day), date_format)