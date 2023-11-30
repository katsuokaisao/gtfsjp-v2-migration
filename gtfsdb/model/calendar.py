import datetime
from sqlalchemy import Column, String, Integer, Date, SmallInteger
from model.base import Base
from model.conversion.string import zenkaku_to_hankaku
from model.validation.time import is_valid_yyyymmdd_format
from model.validation.util import is_required_column

class Calendar(Base):
    filename = 'calendar.txt'
    __tablename__ = 'calendars'

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(String(255), index=True, nullable=False)
    monday = Column(SmallInteger, nullable=False)
    tuesday = Column(SmallInteger, nullable=False)
    wednesday = Column(SmallInteger, nullable=False)
    thursday = Column(SmallInteger, nullable=False)
    friday = Column(SmallInteger, nullable=False)
    saturday = Column(SmallInteger, nullable=False)
    sunday = Column(SmallInteger, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    def validate_record(row_series):
        required_columns = ['service_id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'start_date', 'end_date']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        enum_columns = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for column in enum_columns:
            enabled = row_series[column]
            enabled = zenkaku_to_hankaku(enabled)
            if not enabled.isdigit():
                return False, f"column {column} should be digit: {enabled}"
            if enabled not in ['0', '1']:
                return False, f"column {column} should be 0 or 1"

        yyyymmdd_format_columns = ['start_date', 'end_date']
        for column in yyyymmdd_format_columns:
            date = row_series[column]
            date = zenkaku_to_hankaku(date)
            if not is_valid_yyyymmdd_format(date):
                return False, f"column {column} is not valid yyyymmdd format: {date}"

        return True, None

    def create_instance_from_series(row_series):
        service_id = row_series['service_id']
        monday = row_series['monday']
        tuesday = row_series['tuesday']
        wednesday = row_series['wednesday']
        thursday = row_series['thursday']
        friday = row_series['friday']
        saturday = row_series['saturday']
        sunday = row_series['sunday']
        start_date = row_series['start_date']
        end_date = row_series['end_date']

        monday = zenkaku_to_hankaku(monday)
        monday = int(monday)
        tuesday = zenkaku_to_hankaku(tuesday)
        tuesday = int(tuesday)
        wednesday = zenkaku_to_hankaku(wednesday)
        wednesday = int(wednesday)
        thursday = zenkaku_to_hankaku(thursday)
        thursday = int(thursday)
        friday = zenkaku_to_hankaku(friday)
        friday = int(friday)
        saturday = zenkaku_to_hankaku(saturday)
        saturday = int(saturday)
        sunday = zenkaku_to_hankaku(sunday)
        sunday = int(sunday)

        start_date = zenkaku_to_hankaku(start_date)
        start_date = datetime.datetime.strptime(start_date, '%Y%m%d')
        end_date = zenkaku_to_hankaku(end_date)
        end_date = datetime.datetime.strptime(end_date, '%Y%m%d')

        return Calendar(
            service_id=service_id,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            start_date=start_date,
            end_date=end_date,
        )
