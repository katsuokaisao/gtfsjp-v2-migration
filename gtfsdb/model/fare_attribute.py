from sqlalchemy import Column, String, Integer, SmallInteger
from model.base import Base


class FareAttribute(Base):
    filename = 'fare_attributes.txt'
    __tablename__ = 'fare_attributes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_fare_id = Column(Integer, index=True, nullable=False)
    fare_id = Column(String(255), index=True, nullable=False)
    price = Column(Integer, nullable=False)
    currency_type = Column(String(10), nullable=False) # JPY
    payment_method = Column(SmallInteger, nullable=False) # 0,1
    transfers = Column(SmallInteger, nullable=False) # 0,1,2,3(空白)
    transfer_duration = Column(Integer)
