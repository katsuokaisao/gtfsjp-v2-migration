from sqlalchemy import Column, Integer, String, Index
from model.base import Base


class Transfer(Base):
    filename = 'transfers.txt'
    __tablename__ = 'transfers'
    __table_args__ = (
        Index('idx_transfers_from_stop_id', 'from_stop_id', 'transfer_type'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_stop_id = Column(String(255), nullable=False)
    to_stop_id = Column(String(255), nullable=False)
    system_from_stop_id = Column(Integer, nullable=False)
    system_to_stop_id = Column(Integer, nullable=False)
    transfer_type = Column(Integer, nullable=False) # 0,1,2,3
    min_transfer_time = Column(Integer) # s
