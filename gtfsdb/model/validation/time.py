import datetime


def is_valid_yyyymmdd_format(date_string):
    if len(date_string) != 8: # "2023011"のような不完全な形式（YYYYMDD）が有効と判定されるのを防ぐ
        return False
    try:
        datetime.datetime.strptime(date_string, '%Y%m%d')
        return True
    except ValueError:
        return False

def is_valid_hhmmss_format(time_string):
    if len(time_string) != 7 and len(time_string) != 8:
        return False
    try:
        datetime.datetime.strptime(time_string, "%H:%M:%S")
        return True
    except ValueError:
        return False
