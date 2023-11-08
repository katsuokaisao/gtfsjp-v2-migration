from sqlalchemy import Column, String, Integer
from model.base import Base


class OfficeJP(Base):
    filename = 'office_jp.txt'
    __tablename__ = 'office_jps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    office_id = Column(String(255), index=True, nullable=False)
    office_name = Column(String(255), nullable=False)
    office_url = Column(String(255))
    office_phone = Column(String(50))
