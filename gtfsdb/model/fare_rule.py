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

    @classmethod
    def validate_record(row_series, alias):
        required_columns = ['fare_id']
        for column in required_columns:
            if column not in row_series:
                return False, f"column {column} is required"
            if not row_series[column]:
                return False, f"column {column} is required"

        if 'contains_id' in row_series:
            if row_series['contains_id']:
                print(f"column contains_id is not used: {row_series['contains_id']}")

        return True, None

    @classmethod
    def create_instance_from_series(row_series, alias):
        fare_id = row_series['fare_id']
        route_id = row_series.get('route_id', None)
        origin_id = row_series.get('origin_id', None)
        destination_id = row_series.get('destination_id', None)
        contains_id = row_series.get('contains_id', None)

        system_fare_id = alias['system_fare_id'].get(fare_id, None)
        system_route_id = alias['system_route_id'].get(route_id, None) if route_id else None

        return FareRule(
            system_fare_id=system_fare_id,
            fare_id=fare_id,
            system_route_id=system_route_id,
            route_id=route_id,
            origin_id=origin_id,
            destination_id=destination_id,
            contains_id=contains_id,
        )
