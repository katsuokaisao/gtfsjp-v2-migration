import pytz


def is_valid_timezone(tz_string):
    """入力された文字列が有効なタイムゾーンであるかを確認する"""
    return tz_string in pytz.all_timezones
