from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship
from model.base import Base
from model.conversion.string import zenkaku_to_hankaku


class Trip(Base):
    filename = 'trips.txt'
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(String(255), unique=True, index=True, nullable=False)
    system_route_id = Column(Integer, index=True, nullable=False)
    route_id = Column(String(255), nullable=False)
    system_service_id = Column(Integer, nullable=False)
    service_id = Column(String(255), nullable=False)
    trip_headsign = Column(String(255), index=True)
    trip_short_name = Column(String(255))
    direction_id = Column(SmallInteger) # 0 or 1
    block_id = Column(String(255))
    system_shape_id = Column(Integer, nullable=True)
    shape_id = Column(String(255), nullable=True)
    wheelchair_accessible = Column(SmallInteger) # 0 or 1 or 2
    bikes_allowed = Column(SmallInteger) # 0 or 1 or 2

    jp_trip_desc = Column(String(255))
    jp_trip_desc_symbol = Column(String(255))
    jp_office_id = Column(String(255), nullable=True)
    system_jp_office_id = Column(Integer, nullable=True)

    stop_times = relationship(
        'StopTime',
        primaryjoin='Trip.id==StopTime.system_trip_id',
        foreign_keys='(Trip.id)',
        uselist=True, viewonly=True,
        lazy="joined", innerjoin=False,
        order_by='StopTime.stop_sequence',
    )

    calendars = relationship(
        'Calendar',
        primaryjoin='Trip.system_service_id==Calendar.id',
        foreign_keys='(Trip.system_service_id)',
        uselist=False, viewonly=True,
        lazy="joined", innerjoin=False,
    )

    calendar_dates = relationship(
        'CalendarDate',
        primaryjoin='Trip.id==CalendarDate.system_service_id',
        foreign_keys='(Trip.id)',
        uselist=True, viewonly=True,
        lazy="joined", innerjoin=False,
    )

    office_jp = relationship(
        'OfficeJP',
        primaryjoin='Trip.system_jp_office_id==OfficeJP.id',
        foreign_keys='(Trip.system_jp_office_id)',
        uselist=False, viewonly=True,
        lazy="joined", innerjoin=False,
    )

    frequencies = relationship(
        'Frequency',
        primaryjoin='Trip.id==Frequency.system_trip_id',
        foreign_keys='(Trip.id)',
        uselist=True, viewonly=True,
        lazy="joined", innerjoin=False,
    )

    shapes = relationship(
        'Shape',
        primaryjoin='Trip.system_shape_id==Shape.id',
        foreign_keys='(Trip.system_shape_id)',
        uselist=True, viewonly=True,
        lazy="joined", innerjoin=False,
    )

    @classmethod
    def validate_record(row_series, alias):
        required_columns = ['trip_id', 'route_id', 'service_id']
        for column in required_columns:
            if column not in row_series:
                return False, f"column {column} is required"
            if not row_series[column]:
                return False, f"column {column} is required"

        digit_columns = ['direction_id', 'wheelchair_accessible', 'bikes_allowed']
        for column in digit_columns:
            if column in row_series:
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

    @classmethod
    def create_instance_from_series(row_series, alias):
        trip_id = row_series['trip_id']
        route_id = row_series['route_id']
        service_id = row_series['service_id']
        trip_headsign = row_series.get('trip_headsign', None)
        trip_short_name = row_series.get('trip_short_name', None)
        direction_id = row_series.get('direction_id', None)
        block_id = row_series.get('block_id', None)
        shape_id = row_series.get('shape_id', None)
        wheelchair_accessible = row_series.get('wheelchair_accessible', None)
        bikes_allowed = row_series.get('bikes_allowed', None)

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
