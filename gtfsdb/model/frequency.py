from sqlalchemy import Column, String, Integer, SmallInteger
from model.base import Base
from model.conversion.string import zenkaku_to_hankaku
from model.validation.time import is_valid_hhmmss_format
from model.validation.util import is_required_column, check_nan_or_falsy


class Frequency(Base):
    filename = 'frequencies.txt'
    __tablename__ = 'frequencies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(String(255), nullable=False)
    start_time = Column(String(8), nullable=False)
    end_time = Column(String(8), nullable=False)
    headway_secs = Column(Integer, nullable=False)
    exact_times = Column(SmallInteger) # 0 or 1

    def validate_record(row_series):
        required_columns = ['trip_id', 'start_time', 'end_time', 'headway_secs']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        yyyymmdd_format_columns = ['start_time', 'end_time']
        for column in yyyymmdd_format_columns:
            date = row_series[column]
            date = zenkaku_to_hankaku(date)
            if not is_valid_hhmmss_format(date):
                return False, f"column {column} should be HH:MM:SS format: {date}"

        isdigit_columns = ['headway_secs']
        for column in isdigit_columns:
            value = row_series[column]
            value = zenkaku_to_hankaku(value)
            if not value.isdigit():
                return False, f"column {column} should be digit: {value}"

        if 'exact_times' in row_series:
            exact_times = row_series['exact_times']
            exact_times = zenkaku_to_hankaku(exact_times)
            if exact_times and exact_times not in ['0', '1']:
                print(f"column exact_times should be 0 or 1: {exact_times}")

        return True, None

    def create_instance_from_series(row_series):
        trip_id = row_series['trip_id']
        start_time = row_series['start_time']
        end_time = row_series['end_time']
        headway_secs = row_series['headway_secs']
        exact_times = row_series.get('exact_times', None)
        exact_times = None if check_nan_or_falsy(row_series, 'exact_times') else row_series['exact_times']

        start_time = zenkaku_to_hankaku(start_time)
        end_time = zenkaku_to_hankaku(end_time)
        headway_secs = int(zenkaku_to_hankaku(headway_secs))
        exact_times = int(zenkaku_to_hankaku(exact_times)) if exact_times else None

        return Frequency(
            trip_id=trip_id,
            start_time=start_time,
            end_time=end_time,
            headway_secs=headway_secs,
            exact_times=exact_times,
        )
