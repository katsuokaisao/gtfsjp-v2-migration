from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from model.base import Base


class Agency(Base):
    filename = 'agency.txt'
    __tablename__ = 'agencies'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agency_id = Column(String(255), unique=True, index=True, nullable=False)
    agency_name = Column(String(255), index=True, nullable=False)
    agency_url = Column(String(255), nullable=False)
    agency_timezone = Column(String(50), nullable=False) # Asia/Tokyo
    agency_lang = Column(String(10)) # ja
    agency_phone = Column(String(50))
    agency_fare_url = Column(String(255))
    agency_email = Column(String(255))

    routes = relationship(
        'Route',
        primaryjoin='Agency.id==Route.system_agency_id',
        foreign_keys='(Agency.id)',
        uselist=True, viewonly=True,
        lazy="joined", innerjoin=True,
    )

    agency_jp = relationship(
        'AgencyJP',
        primaryjoin='Agency.id==AgencyJP.system_agency_id',
        foreign_keys='(Agency.id)',
        uselist=False, viewonly=True,
        lazy="joined", innerjoin=True,
    )
