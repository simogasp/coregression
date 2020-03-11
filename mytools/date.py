import datetime
from typing import Union, Iterable as typeIterable
from collections.abc import Iterable


def day_of_year_to_date(day: Union[int, float, typeIterable], year: Union[int, float] = None) -> Union[
        datetime.datetime, typeIterable[datetime.datetime]]:
    """
    Given the day(s) of the year it returns the corresponding datetime(s)
    Args:
        day (int or typeIterable): the day of the year [1 366]
        year (int or float): the year, if None, the current year is assumed

    Returns:
        The associated datetime
    """
    if year is None:
        year = datetime.datetime.now().year

    if isinstance(day, Iterable):
        return list(day_of_year_to_date(d, year) for d in day)
    else:
        return datetime.datetime(int(year), 1, 1) + datetime.timedelta(days=int(day - 1))


def date_to_string(date: Union[datetime.datetime, typeIterable[datetime.datetime]], date_format: str = '%d %b'):
    if isinstance(date, Iterable):
        return list(date_to_string(d, date_format) for d in date)
    else:
        return date.strftime(date_format)


def date_to_day_of_year(date: Union[datetime.datetime, typeIterable[datetime.datetime]])\
        -> Union[int, typeIterable[int]]:
    if isinstance(date, list):
        return list(date_to_day_of_year(d) for d in date)
    else:
        delta = date - datetime.datetime(date.year, 1, 1)
        return delta.days + 1


def str_to_day_of_year(date: Union[str, list], date_format: str = '%m/%d/%y') -> Union[int, list]:
    if isinstance(date, list):
        days = list(str_to_day_of_year(d, date_format) for d in date)
        return days
    else:
        d = datetime.datetime.strptime(date, date_format)
        return date_to_day_of_year(d)


def day_of_year_to_string(day: Union[int, float, typeIterable], date_format: str = '%d %b') -> Union[
        str, typeIterable[str]]:
    if isinstance(day, Iterable):
        return list(day_of_year_to_string(d, date_format) for d in day)
    else:
        return date_to_string(day_of_year_to_date(day), date_format)
