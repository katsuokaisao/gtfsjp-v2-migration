from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship
from model.base import Base


class Route(Base):
    filename = 'routes.txt'
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(String(255), unique=True, index=True, nullable=False)
    system_agency_id = Column(Integer, index=True, nullable=False)
    agency_id = Column(String(255), nullable=False)
    route_short_name = Column(String(255)) # route_short_name or route_long_name must be specified
    route_long_name = Column(String(255))  # route_short_name or route_long_name must be specified
    route_desc = Column(String(1023))
    route_type = Column(SmallInteger, nullable=False)
    route_url = Column(String(255))
    route_color = Column(String(6))
    route_text_color = Column(String(6))
    jp_parent_route_id = Column(String(255))

    route_jp = relationship(
        'RouteJP',
        primaryjoin='Route.id==RouteJP.system_route_id',
        foreign_keys='(Route.id)',
        uselist=False, viewonly=True,
        lazy="joined", innerjoin=True,
    )

    trips = relationship(
        'Trip',
        primaryjoin='Route.id==Trip.system_route_id',
        foreign_keys='(Route.id)',
        uselist=True, viewonly=True,
        lazy="joined", innerjoin=True,
    )
