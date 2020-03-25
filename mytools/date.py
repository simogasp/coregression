import datetime
from typing import Union, List, Iterable as typeIterable
from collections.abc import Iterable

format_ISO8601 = '%Y-%m-%dT%H:%M:%S'
format_mmddyy = '%m/%d/%y'
format_ddmmyy = '%d/%m/%y'
format_mmmdd = '%d %b'


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


def date_to_string(date: Union[datetime.datetime, typeIterable[datetime.datetime]], date_format: str = format_mmmdd):
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


def str_convert_date(date: Union[str, List[str]], format_from: str, format_to: str) -> Union[str, List[str]]:
    if isinstance(date, list):
        dates = list(str_convert_date(d, format_from, format_to) for d in date)
        return dates
    else:
        return datetime.datetime.strptime(date, format_from).strftime(format_to)


def str_convert_mdy_to_dmy(date: Union[str, List[str]]) -> Union[str, List[str]]:
    """

    Args:
        date (str or list of str): the date(s) in mm/dd/yy format

    Returns:
        dates in dd/mm/yy
    """
    return str_convert_date(date, format_from=format_mmddyy, format_to=format_ddmmyy)


def str_to_day_of_year(date: Union[str, list], date_format: str = format_mmddyy) -> Union[int, list]:
    if isinstance(date, list):
        days = list(str_to_day_of_year(d, date_format) for d in date)
        return days
    else:
        d = datetime.datetime.strptime(date, date_format)
        return date_to_day_of_year(d)


def day_of_year_to_string(day: Union[int, float, typeIterable], date_format: str = format_mmmdd) -> Union[
        str, typeIterable[str]]:
    if isinstance(day, Iterable):
        return list(day_of_year_to_string(d, date_format) for d in day)
    else:
        return date_to_string(day_of_year_to_date(day), date_format)
