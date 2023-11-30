from sqlalchemy import Column, Integer, String
from model.base import Base
from model.validation.util import is_required_column


class RouteJP(Base):
    filename = 'routes_jp.txt'
    __tablename__ = 'route_jps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(String(255), nullable=False)
    route_update_date = Column(String(255))
    origin_stop = Column(String(255))
    via_stop = Column(String(255))
    destination_stop = Column(String(255))

    def validate_record(row_series):
        required_columns = ['route_id']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        return True, None

    def create_instance_from_series(row_series):
        route_id = row_series['route_id']
        route_update_date = row_series.get('route_update_date', None)
        origin_stop = row_series.get('origin_stop', None)
        via_stop = row_series.get('via_stop', None)
        destination_stop = row_series.get('destination_stop', None)

        return RouteJP(
            route_id=route_id,
            route_update_date=route_update_date,
            origin_stop=origin_stop,
            via_stop=via_stop,
            destination_stop=destination_stop,
        )
