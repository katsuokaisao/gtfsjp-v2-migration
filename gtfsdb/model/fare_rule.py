from sqlalchemy import Column, String, Integer, Index
from model.base import Base
from model.validation.util import is_required_column, check_nan_or_falsy


class FareRule(Base):
    filename = 'fare_rules.txt'
    __tablename__ = 'fare_rules'
    __table_args__ = (
        Index('idx_origin_id_destination_id', 'origin_id', 'destination_id'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    fare_id = Column(String(255), index=True, nullable=False)
    route_id = Column(String(255))
    origin_id = Column(String(255))
    destination_id = Column(String(255))
    contains_id = Column(String(255)) # 使用しない

    def validate_record(row_series):
        required_columns = ['fare_id']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        return True, None

    def create_instance_from_series(row_series):
        fare_id = row_series['fare_id']
        route_id = row_series.get('route_id', None)
        origin_id = row_series.get('origin_id', None)
        destination_id = row_series.get('destination_id', None)
        contains_id = row_series.get('contains_id', None)

        return FareRule(
            fare_id=fare_id,
            route_id=route_id,
            origin_id=origin_id,
            destination_id=destination_id,
            contains_id=contains_id,
        )
