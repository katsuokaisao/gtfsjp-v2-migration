from sqlalchemy import Column, String, Integer, SmallInteger
from sqlalchemy.orm import relationship
from model.base import Base


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