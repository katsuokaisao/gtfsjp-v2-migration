import datetime
from pandas import isna
from sqlalchemy import Column, String, Integer, Date, SmallInteger
from model.base import Base
from model.conversion.string import zenkaku_to_hankaku
from model.validation.time import is_valid_yyyymmdd_format
from model.validation.util import is_required_column, check_nan_or_falsy

class CalendarDate(Base):
    filename = 'calendar_dates.txt'
    __tablename__ = 'calendar_dates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(String(255), unique=True, index=True, nullable=False)
    date = Column(Date,  index=True, nullable=False) # YYYYMMDD
    exception_type = Column(SmallInteger, nullable=False) # 1 or 2

    def validate_record(row_series):
        required_columns = ['service_id', 'date', 'exception_type']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        yyyymmdd_format_columns = ['date']
        for column in yyyymmdd_format_columns:
            if check_nan_or_falsy(row_series, column):
                continue
            date = row_series[column]
            date = zenkaku_to_hankaku(date)
            if not is_valid_yyyymmdd_format(date):
                return False, f"column {column} is not valid yyyymmdd format: {date}"

        exception_type = row_series['exception_type']
        exception_type = zenkaku_to_hankaku(exception_type)
        if not exception_type.isdigit():
            return False, f"column exception_type should be integer"
        if exception_type not in ['1', '2']:
            return False, f"column exception_type should be 1 or 2"

        return True, None

    def create_instance_from_series(row_series):
        service_id = row_series['service_id']
        date = row_series['date']
        exception_type = row_series['exception_type']

        date = zenkaku_to_hankaku(date)
        date = datetime.datetime.strptime(date, '%Y%m%d')

        exception_type = zenkaku_to_hankaku(exception_type)
        exception_type = int(exception_type)

        return CalendarDate(
            service_id=service_id,
            date=date,
            exception_type=exception_type,
        )
