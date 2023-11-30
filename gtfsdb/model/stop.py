from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from model.base import Base
from model.validation.location import is_valid_longitude, is_valid_latitude
from model.validation.url import is_valid_url
from model.conversion.string import zenkaku_to_hankaku
from model.validation.util import is_required_column, check_nan_or_falsy


class Stop(Base):
    filename = 'stops.txt'
    __tablename__ = 'stops'

    id = Column(Integer, primary_key=True, autoincrement=True)
    stop_id = Column(String(255),  nullable=False)
    stop_code = Column(String(50))
    stop_name = Column(String(255), nullable=False)
    stop_desc = Column(String(255))
    stop_lat = Column(Numeric(9, 6), nullable=False)
    stop_lon = Column(Numeric(9, 6), nullable=False)
    zone_id = Column(String(50))
    stop_url = Column(String(255))
    location_type = Column(Integer, default=0)
    parent_station = Column(String(255))
    stop_timezone = Column(String(50)) # 不要
    wheelchair_boarding = Column(String(255)) # 不要
    platform_code = Column(String(50))

    stop_times = relationship(
        'StopTime',
        primaryjoin='Stop.id == StopTime.system_stop_id',
        foreign_keys='(Stop.id)',
        uselist=True, viewonly=True
    )

    def validate_record(row_series, alias):
        required_columns = ['stop_id', 'stop_name', 'stop_lat', 'stop_lon']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        lat_columns = ['stop_lat']
        for column in lat_columns:
            value = row_series[column]
            value = zenkaku_to_hankaku(value)
            if not is_valid_latitude(value):
                return False, f"column {column} should be latitude: {value}"

        lon_columns = ['stop_lon']
        for column in lon_columns:
            value = row_series[column]
            value = zenkaku_to_hankaku(value)
            if not is_valid_longitude(value):
                return False, f"column {column} should be longitude: {value}"

        url_columns = ['stop_url']
        for column in url_columns:
            if check_nan_or_falsy(row_series, column):
                continue
            value = zenkaku_to_hankaku(value)
            if not is_valid_url(value):
                print(f"column {column} should be url: {value}")

        enum_columns = ['location_type']
        for column in enum_columns:
            if check_nan_or_falsy(row_series, column):
                continue
            value = row_series[column]
            value = zenkaku_to_hankaku(value)
            if not value.isdigit():
                print(f"column {column} should be digit: {value}")
            if value not in ['0', '1']:
                print(f"column {column} should be 0 or 1: {value}")

        return True, None

    def create_instance_from_series(row_series, alias):
        stop_id = row_series['stop_id']
        stop_code = row_series.get('stop_code', None)
        stop_name = row_series['stop_name']
        stop_desc = row_series.get('stop_desc', None)
        stop_lat = row_series['stop_lat']
        stop_lon = row_series['stop_lon']
        zone_id = row_series.get('zone_id', None)
        stop_url = row_series.get('stop_url', None)
        location_type = row_series.get('location_type', None)
        parent_station = row_series.get('parent_station', None)
        stop_timezone = row_series.get('stop_timezone', None)
        wheelchair_boarding = row_series.get('wheelchair_boarding', None)
        platform_code = row_series.get('platform_code', None)

        stop_lat = zenkaku_to_hankaku(stop_lat)
        stop_lon = zenkaku_to_hankaku(stop_lon)
        stop_lat = float(stop_lat)
        stop_lon = float(stop_lon)

        if location_type:
            location_type = zenkaku_to_hankaku(location_type)
            location_type = int(location_type)

        stop_url = zenkaku_to_hankaku(stop_url)

        return Stop(
            stop_id=stop_id,
            stop_code=stop_code,
            stop_name=stop_name,
            stop_desc=stop_desc,
            stop_lat=stop_lat,
            stop_lon=stop_lon,
            zone_id=zone_id,
            stop_url=stop_url,
            location_type=location_type,
            parent_station=parent_station,
            stop_timezone=stop_timezone,
            wheelchair_boarding=wheelchair_boarding,
            platform_code=platform_code,
        )
