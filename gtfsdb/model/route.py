from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship
from model.base import Base
from model.validation.url import is_valid_url
from model.validation.color import is_valid_color
from model.conversion.string import zenkaku_to_hankaku
from model.validation.util import is_required_column, check_nan_or_falsy


class Route(Base):
    filename = 'routes.txt'
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(String(255), unique=True, index=True, nullable=False)
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
        primaryjoin='Route.route_id==RouteJP.route_id',
        foreign_keys='(Route.route_id)',
        uselist=False, viewonly=True,
        lazy="joined", innerjoin=True,
    )

    trips = relationship(
        'Trip',
        primaryjoin='Route.route_id==Trip.route_id',
        foreign_keys='(Route.route_id)',
        uselist=True, viewonly=True,
        lazy="joined", innerjoin=True,
    )

    def validate_record(row_series):
        required_columns = ['route_id', 'agency_id', 'route_type']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        route_short_name = row_series.get('route_short_name', None)
        route_long_name = row_series.get('route_long_name', None)
        if not route_short_name and not route_long_name:
            return False, f"either route_short_name or route_long_name must be specified"

        isdigit_columns = ['route_type']
        for column in isdigit_columns:
            value = row_series[column]
            value = zenkaku_to_hankaku(value)
            if not value.isdigit():
                return False, f"column {column} should be digit: {value}"

        url_columns = ['route_url']
        for column in url_columns:
            if check_nan_or_falsy(row_series, column):
                continue
            url = row_series[column]
            url = zenkaku_to_hankaku(url)
            if not is_valid_url(url):
                print(f"column {column} should be url: {url}")

        color_columns = ['route_color', 'route_text_color']
        for column in color_columns:
            if check_nan_or_falsy(row_series, column):
                continue
            color = row_series[column]
            color = zenkaku_to_hankaku(color)
            if not is_valid_color(color):
                print(f"column {column} should be color code: {color}")

        return True, None

    def create_instance_from_series(row_series):
        route_id = row_series['route_id']
        agency_id = row_series['agency_id']
        route_type = row_series['route_type']

        route_short_name = row_series.get('route_short_name', None)
        route_long_name = row_series.get('route_long_name', None)
        route_desc = row_series.get('route_desc', None)
        route_url = row_series.get('route_url', None)
        route_color = row_series.get('route_color', None)
        route_text_color = row_series.get('route_text_color', None)
        jp_parent_route_id = row_series.get('jp_parent_route_id', None)

        route_type = int(zenkaku_to_hankaku(route_type))

        return Route(
            route_id=route_id,
            agency_id=agency_id,
            route_short_name=route_short_name,
            route_long_name=route_long_name,
            route_desc=route_desc,
            route_type=route_type,
            route_url=route_url,
            route_color=route_color,
            route_text_color=route_text_color,
            jp_parent_route_id=jp_parent_route_id,
        )
