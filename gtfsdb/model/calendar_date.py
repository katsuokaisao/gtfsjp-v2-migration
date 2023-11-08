from sqlalchemy import Column, String, Integer, Date, SmallInteger
from model.base import Base


class CalendarDate(Base):
    filename = 'calendar_dates.txt'
    __tablename__ = 'calendar_dates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_service_id = Column(Integer, index=True, nullable=False)
    service_id = Column(String(255), unique=True, index=True, nullable=False)
    date = Column(Date,  index=True, nullable=False) # YYYYMMDD
    exception_type = Column(SmallInteger, nullable=False) # 1 or 2
