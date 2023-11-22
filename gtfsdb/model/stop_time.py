from sqlalchemy import Column, String, Integer, SmallInteger
from sqlalchemy.orm import relationship
from model.base import Base
from model.validation.time import is_valid_hhmmss_format
from model.conversion.string import zenkaku_to_hankaku


class StopTime(Base):
    filename = 'stop_times.txt'
    __tablename__ = 'stop_times'

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_trip_id = Column(Integer, index=True, nullable=False)
    trip_id = Column(String(255), nullable=False)
    arrival_time = Column(String(9), nullable=False) # 00:00:00
    departure_time = Column(String(9), nullable=False) # 00:00:00
    system_stop_id = Column(Integer, index=True, nullable=False)
    stop_id = Column(String(255), nullable=False)
    stop_sequence = Column(Integer, nullable=False)
    stop_headsign = Column(String(255))
    pickup_type = Column(SmallInteger, default=0)
    drop_off_type = Column(SmallInteger, default=0)
    shape_dist_traveled = Column(Integer)
    timepoint = Column(SmallInteger, index=True, default=0) # 日本では使用しない

    stop = relationship(
        'Stop',
        primaryjoin='StopTime.system_stop_id == Stop.id',
        foreign_keys='(StopTime.system_stop_id)',
        uselist=False, viewonly=True
    )

    trip = relationship(
        'Trip',
        primaryjoin='StopTime.system_trip_id == Trip.id',
        foreign_keys='(StopTime.system_trip_id)',
        uselist=False, viewonly=True
    )

    @classmethod
    def validate_record(row_series, alias):
        required_columns = ['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence']
        for column in required_columns:
            if column not in row_series:
                return False, f"column {column} is required"
            if not row_series[column]:
                return False, f"column {column} is required"

        hhmmss_columns = ['arrival_time', 'departure_time']
        for column in hhmmss_columns:
            value = row_series[column]
            if not is_valid_hhmmss_format(value):
                return False, f"column {column} should be HH:MM:SS format: {value}"

        enum_columns = ['pickup_type', 'drop_off_type']
        for column in enum_columns:
            if column in row_series:
                value = row_series[column]
                value = zenkaku_to_hankaku(value)
                if value not in ['0', '1', '2', '3']:
                    print(f"column {column} should be 0, 1, 2 or 3: {value}")

        return True, None

    @classmethod
    def create_instance_from_series(row_series, alias):
        trip_id = row_series['trip_id']
        arrival_time = row_series['arrival_time']
        departure_time = row_series['departure_time']
        stop_id = row_series['stop_id']
        stop_sequence = row_series['stop_sequence']
        stop_headsign = row_series.get('stop_headsign', None)
        pickup_type = row_series.get('pickup_type', None)
        drop_off_type = row_series.get('drop_off_type', None)
        shape_dist_traveled = row_series.get('shape_dist_traveled', None)
        timepoint = row_series.get('timepoint', None)

        arrival_time = zenkaku_to_hankaku(arrival_time)
        departure_time = zenkaku_to_hankaku(departure_time)
        stop_sequence = zenkaku_to_hankaku(stop_sequence)

        stop_sequence = int(stop_sequence)
        pickup_type = int(pickup_type) if pickup_type else None
        drop_off_type = int(drop_off_type) if drop_off_type else None
        shape_dist_traveled = int(shape_dist_traveled) if shape_dist_traveled else None

        return StopTime(
            trip_id=trip_id,
            arrival_time=arrival_time,
            departure_time=departure_time,
            stop_id=stop_id,
            stop_sequence=stop_sequence,
            stop_headsign=stop_headsign,
            pickup_type=pickup_type,
            drop_off_type=drop_off_type,
            shape_dist_traveled=shape_dist_traveled,
            timepoint=timepoint,
        )
