from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from model.base import Base


class Stop(Base):
    filename = 'stops.txt'
    __tablename__ = 'stops'

    id = Column(Integer, primary_key=True, autoincrement=True)
    stop_id = Column(String(255),  nullable=False)
    stop_code = Column(String(50))
    stop_name = Column(String(255), nullable=False)
    stop_desc = Column(String(255))
    stop_lat = Column(Numeric(9, 6), nullable=False)
    stop_lon = Column(Numeric(9, 6), nullable=False)
    zone_id = Column(String(50))
    stop_url = Column(String(255))
    location_type = Column(Integer, default=0)
    parent_station = Column(String(255))
    stop_timezone = Column(String(50)) # 不要
    wheelchair_boarding = Column(Integer) # 不要
    platform_code = Column(String(50))

    stop_times = relationship(
        'StopTime',
        primaryjoin='Stop.id == StopTime.system_stop_id',
        foreign_keys='(Stop.id)',
        uselist=True, viewonly=True
    )
