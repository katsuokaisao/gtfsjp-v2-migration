from sqlalchemy import Column, Integer, String
from model.base import Base


class RouteJP(Base):
    filename = 'routes_jp.txt'
    __tablename__ = 'route_jps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_route_id = Column(Integer, index=True, nullable=False)
    route_id = Column(String(255), nullable=False)
    route_update_date = Column(String(255))
    origin_stop = Column(String(255))
    via_stop = Column(String(255))
    destination_stop = Column(String(255))
