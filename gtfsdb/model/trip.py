from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship
from model.base import Base


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

