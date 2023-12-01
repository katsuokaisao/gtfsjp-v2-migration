from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship
from model.base import Base
from model.conversion.string import zenkaku_to_hankaku
from model.validation.util import is_required_column, check_nan_or_falsy


class Trip(Base):
    filename = 'trips.txt'
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(String(255), unique=True, index=True, nullable=False)
    route_id = Column(String(255), nullable=False)
    service_id = Column(String(255), nullable=False)
    trip_headsign = Column(String(255), index=True)
    trip_short_name = Column(String(255))
    direction_id = Column(SmallInteger) # 0 or 1
    block_id = Column(String(255))
    shape_id = Column(String(255), nullable=True)
    wheelchair_accessible = Column(SmallInteger) # 0 or 1 or 2
    bikes_allowed = Column(SmallInteger) # 0 or 1 or 2

    jp_trip_desc = Column(String(255))
    jp_trip_desc_symbol = Column(String(255))
    jp_office_id = Column(String(255), nullable=True)

    stop_times = relationship(
        'StopTime',
        primaryjoin='Trip.trip_id==StopTime.trip_id',
        foreign_keys='(Trip.trip_id)',
        uselist=True, viewonly=True,
        lazy="joined", innerjoin=False,
        order_by='StopTime.stop_sequence',
    )

    calendars = relationship(
        'Calendar',
        primaryjoin='Trip.service_id==Calendar.service_id',
        foreign_keys='(Trip.service_id)',
        uselist=False, viewonly=True,
        lazy="joined", innerjoin=False,
    )

    calendar_dates = relationship(
        'CalendarDate',
        primaryjoin='Trip.service_id==CalendarDate.service_id',
        foreign_keys='(Trip.service_id)',
        uselist=True, viewonly=True,
        lazy="joined", innerjoin=False,
    )

    office_jp = relationship(
        'OfficeJP',
        primaryjoin='Trip.jp_office_id==OfficeJP.office_id',
        foreign_keys='(Trip.jp_office_id)',
        uselist=False, viewonly=True,
        lazy="joined", innerjoin=False,
    )

    frequencies = relationship(
        'Frequency',
        primaryjoin='Trip.trip_id==Frequency.trip_id',
        foreign_keys='(Trip.trip_id)',
        uselist=True, viewonly=True,
        lazy="joined", innerjoin=False,
    )

    shapes = relationship(
        'Shape',
        primaryjoin='Trip.shape_id==Shape.shape_id',
        foreign_keys='(Trip.shape_id)',
        uselist=True, viewonly=True,
        lazy="joined", innerjoin=False,
    )

    def validate_record(row_series):
        required_columns = ['trip_id', 'route_id', 'service_id']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        digit_columns = ['direction_id', 'wheelchair_accessible', 'bikes_allowed']
        for column in digit_columns:
            if check_nan_or_falsy(row_series, column):
                continue
            value = row_series[column]
            value = zenkaku_to_hankaku(value)
            if not value.isdigit():
                print(f"column {column} should be digit: {value}")
            if column == 'direction_id':
                if value not in ['0', '1']:
                    print(f"column {column} should be 0 or 1: {value}")
            else:
                if value not in ['0', '1', '2']:
                    print(f"column {column} should be 0, 1 or 2: {value}")

        return True, None

    def create_instance_from_series(row_series):
        trip_id = row_series['trip_id']
        route_id = row_series['route_id']
        service_id = row_series['service_id']

        trip_headsign = None if check_nan_or_falsy(row_series, 'trip_headsign') else row_series['trip_headsign']
        trip_short_name = None if check_nan_or_falsy(row_series, 'trip_short_name') else row_series['trip_short_name']
        direction_id = None if check_nan_or_falsy(row_series, 'direction_id') else row_series['direction_id']
        block_id = None if check_nan_or_falsy(row_series, 'block_id') else row_series['block_id']
        shape_id = None if check_nan_or_falsy(row_series, 'shape_id') else row_series['shape_id']
        wheelchair_accessible = None if check_nan_or_falsy(row_series, 'wheelchair_accessible') else row_series['wheelchair_accessible']
        bikes_allowed = None if check_nan_or_falsy(row_series, 'bikes_allowed') else row_series['bikes_allowed']

        direction_id = int(direction_id) if direction_id else None
        wheelchair_accessible = int(wheelchair_accessible) if wheelchair_accessible else None
        bikes_allowed = int(bikes_allowed) if bikes_allowed else None

        return Trip(
            trip_id=trip_id,
            route_id=route_id,
            service_id=service_id,
            trip_headsign=trip_headsign,
            trip_short_name=trip_short_name,
            direction_id=direction_id,
            block_id=block_id,
            shape_id=shape_id,
            wheelchair_accessible=wheelchair_accessible,
            bikes_allowed=bikes_allowed,
        )
