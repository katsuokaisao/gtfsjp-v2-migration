from sqlalchemy import Column, Integer, String
from model.base import Base


class AgencyJP(Base):
    filename = 'agency_jp.txt'
    __tablename__ = 'agency_jps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_agency_id = Column(Integer, unique=True, nullable=False)
    agency_id = Column(String(255), unique=True, nullable=False)
    agency_official_name = Column(String(255))
    agency_zip_number = Column(Integer)
    agency_address = Column(String(255))
    agency_president_pos = Column(String(50))
    agency_president_name = Column(String(10))
