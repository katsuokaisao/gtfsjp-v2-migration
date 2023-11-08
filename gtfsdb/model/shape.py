from sqlalchemy import Column, String, Integer, Numeric, UniqueConstraint, Index
from model.base import Base


class Shape(Base):
    filename = 'shapes.txt'
    __tablename__ = 'shapes'
    __table_args__ = (
        UniqueConstraint('shape_id', 'shape_pt_sequence', name='shape_id_shape_pt_sequence_key'),
        Index('shape_id_shape_pt_sequence_index', 'shape_id', 'shape_pt_sequence'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    shape_id = Column(String(255), nullable=False)
    shape_pt_lat = Column(Numeric(9, 6), nullable=False)
    shape_pt_lon = Column(Numeric(9, 6), nullable=False)
    shape_pt_sequence = Column(Integer, nullable=False)
    shape_dist_traveled = Column(String(255)) # 使用しない
