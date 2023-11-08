from sqlalchemy import Column, String, Integer, SmallInteger
from model.base import Base


class Frequency(Base):
    filename = 'frequencies.txt'
    __tablename__ = 'frequencies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_trip_id = Column(Integer, index=True, nullable=False)
    trip_id = Column(String(255), nullable=False)
    start_time = Column(String(8), nullable=False)
    end_time = Column(String(8), nullable=False)
    headway_secs = Column(Integer, nullable=False)
    exact_times = Column(SmallInteger) # 0 or 1
