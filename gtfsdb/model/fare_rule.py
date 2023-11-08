from sqlalchemy import Column, String, Integer, Index
from model.base import Base


class FareRule(Base):
    filename = 'fare_rules.txt'
    __tablename__ = 'fare_rules'
    __table_args__ = (
        Index('idx_origin_id_destination_id', 'origin_id', 'destination_id'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_fare_id = Column(Integer, index=True, nullable=False)
    fare_id = Column(String(255), index=True, nullable=False)
    system_route_id = Column(Integer, index=True, nullable=False)
    route_id = Column(String(255))
    origin_id = Column(String(255))
    destination_id = Column(String(255))
    contains_id = Column(String(255)) # 使用しない
