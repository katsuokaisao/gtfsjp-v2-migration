from sqlalchemy import Column, String, Integer, Date, SmallInteger
from model.base import Base


class Calendar(Base):
    filename = 'calendar.txt'
    __tablename__ = 'calendars'

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_service_id = Column(Integer, index=True, nullable=False)
    service_id = Column(String(255), unique=True, index=True, nullable=False)
    monday = Column(SmallInteger, nullable=False)
    tuesday = Column(SmallInteger, nullable=False)
    wednesday = Column(SmallInteger, nullable=False)
    thursday = Column(SmallInteger, nullable=False)
    friday = Column(SmallInteger, nullable=False)
    saturday = Column(SmallInteger, nullable=False)
    sunday = Column(SmallInteger, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
