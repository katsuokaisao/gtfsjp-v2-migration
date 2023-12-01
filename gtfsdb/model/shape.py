from sqlalchemy import Column, String, Integer, Numeric, UniqueConstraint, Index
from model.base import Base
from model.validation.location import is_valid_longitude, is_valid_latitude
from model.conversion.string import zenkaku_to_hankaku
from model.validation.util import is_required_column, check_nan_or_falsy


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

    def validate_record(row_series):
        required_columns = ['shape_id', 'shape_pt_lat', 'shape_pt_lon', 'shape_pt_sequence']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        lat_columns = ['shape_pt_lat']
        for column in lat_columns:
            value = row_series[column]
            value = zenkaku_to_hankaku(value)
            if not is_valid_latitude(value):
                return False, f"column {column} should be latitude: {value}"

        lon_columns = ['shape_pt_lon']
        for column in lon_columns:
            value = row_series[column]
            value = zenkaku_to_hankaku(value)
            if not is_valid_longitude(value):
                return False, f"column {column} should be longitude: {value}"

        digit_columns = ['shape_pt_sequence']
        for column in digit_columns:
            value = row_series[column]
            value = zenkaku_to_hankaku(value)
            if not value.isdigit():
                return False, f"column {column} should be digit: {value}"

        unused_columns = ['shape_dist_traveled']
        for column in unused_columns:
            if check_nan_or_falsy(row_series, column):
                return False, f"column {column} should be unused"

        return True, None

    def create_instance_from_series(row_series):
        shape_id = row_series['shape_id']
        shape_pt_lat = row_series['shape_pt_lat']
        shape_pt_lon = row_series['shape_pt_lon']
        shape_pt_sequence = row_series['shape_pt_sequence']
        shape_dist_traveled = None if check_nan_or_falsy(row_series, 'shape_dist_traveled') else row_series['shape_dist_traveled']

        shape_pt_lat = zenkaku_to_hankaku(shape_pt_lat)
        shape_pt_lon = zenkaku_to_hankaku(shape_pt_lon)
        shape_pt_sequence = zenkaku_to_hankaku(shape_pt_sequence)

        shape_pt_lat = float(shape_pt_lat)
        shape_pt_lon = float(shape_pt_lon)
        shape_pt_sequence = int(shape_pt_sequence)

        return Shape(
            shape_id=shape_id,
            shape_pt_lat=shape_pt_lat,
            shape_pt_lon=shape_pt_lon,
            shape_pt_sequence=shape_pt_sequence,
            shape_dist_traveled=shape_dist_traveled,
        )
