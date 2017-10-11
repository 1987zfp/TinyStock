# -*- coding: utf-8 -*-
from datetime import datetime, timedelta as td

date_format_ymdHM = '%Y-%m-%d %H:%M'
date_format_ymd = '%Y-%m-%d'
date_format_md = '%m-%d'
time_format_HM = '%H:%M:%S'


# 放假开始前1天和放假结束后1天,连续的两个交易日
holidays = {
    '2012-12-31': '2013-01-04',
    '2013-02-08': '2013-02-18',
    '2013-04-03': '2013-04-08',
    '2013-04-28': '2013-05-02',
    '2013-06-07': '2013-06-13',
    '2013-09-18': '2013-09-23',
    '2013-09-30': '2013-10-08',
    '2013-12-31': '2014-01-02',
    '2014-01-30': '2014-02-07',
    '2014-04-04': '2014-04-08',
    '2014-04-30': '2014-05-05',
    '2014-05-30': '2014-06-03',
    '2014-09-05': '2014-09-09',
    '2014-09-30': '2014-10-08',
    '2014-12-31': '2015-01-05',
    '2015-02-17': '2015-02-25',
    '2015-04-03': '2015-04-07',
    '2015-04-30': '2015-05-04',
    '2015-06-19': '2015-06-23',
    '2015-09-02': '2015-09-07',
    '2015-09-30': '2015-10-08',
    '2015-12-31': '2016-01-04',
    '2016-02-05': '2016-02-15',
    '2016-04-01': '2016-04-05',
    '2016-04-29': '2016-05-03',
    '2016-06-08': '2016-06-13',
    '2016-09-14': '2016-09-19',
    '2016-09-30': '2016-10-10',
    '2016-12-30': '2017-01-03',
    '2017-01-26': '2017-02-03',
    '2017-03-31': '2017-04-05',
    '2017-04-28': '2017-05-02',
    '2017-05-26': '2017-05-31',
    '2017-09-29': '2017-10-09'
}


def to_date(date_string):
    return datetime.strptime(date_string, date_format_ymd).date()


def to_time_fs(time_string):
    return datetime.strptime(time_string, time_format_HM).time()


def to_datetime(datetime_string, fmt=date_format_ymdHM):
    return datetime.strptime(datetime_string, fmt)


def to_string(date, date_format=date_format_ymd):
    return date.strftime(date_format)


def get_range_dates(start, end):
    delta = end - start
    weekend = [5, 6]
    lst = []
    for i in range(delta.days + 1):
        # except for weekends
        d = start + td(days=i)
        if d.weekday() in weekend:
            continue
        lst.append(d)
    return lst


def get_range_date_strings(start_string, end_string):
    start = to_date(start_string)
    end = to_date(end_string)
    range_dates = get_range_dates(start, end)

    return [i.strftime(date_format_ymd) for i in range_dates]


def get_next_trading_date(date):
    # 节假日
    date_string = to_string(date)
    if date_string in holidays.keys():
        return to_date(holidays[date_string])
    # 周五 +3天
    if date.weekday() == 4:
        return date + td(days=3)
    # 周六 +2天
    if date.weekday() == 5:
        return date + td(days=2)
    # 周日到周四 +1天
    else:
        return date + td(days=1)


def get_next_trading_date_string(date_string):
    date = to_date(date_string)
    date_next = get_next_trading_date(date)

    return date_next.strftime(date_format_ymd)


def get_range_trading_dates(start, end):
    lst = []
    date_i = start
    while date_i <= end:
        if is_trading_date(date_i):
            lst.append(date_i)
        date_i = get_next_trading_date(date_i)
    return lst


def get_range_trading_date_strings(start_string, end_string):
    start = to_date(start_string)
    end = to_date(end_string)
    lst = get_range_trading_dates(start, end)
    return [to_string(i) for i in lst]


def is_trading_date(date):
    # 周末
    if date.weekday() in [5, 6]:
        return False
    for date1_string in holidays.keys():
        date1 = to_date(date1_string)
        date2 = to_date(holidays[date1_string])
        # 节假日
        if date1 < date < date2:
            return False
    return True


def is_seq_trading_day(date1, date2):
    # 差1天
    if date2 - date1 == td(days=1):
        return True
    # 周1和周5
    if date2 - date1 == td(days=3) and date2.weekday() == 0:
        return True
    # 节假日
    d1_string = to_string(date1)
    d2_string = to_string(date2)
    if holidays.has_key(d1_string) and holidays[d1_string] == d2_string:
        return True
    return False
