from pandas import isna

def is_required_column(row_series, column):
    if column not in row_series:
        return False
    v = row_series[column]
    if isna(v) or not v:
        return False
    return True

def check_nan_or_falsy(row_series, column):
    if column not in row_series:
        return True
    v = row_series[column]
    if isna(v) or not v:
        return True
    return False