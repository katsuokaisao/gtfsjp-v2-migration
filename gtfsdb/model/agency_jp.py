from pandas import isna
from sqlalchemy import Column, Integer, String
from model.base import Base
from model.conversion.string import zenkaku_to_hankaku
from model.validation.address import is_valid_japanese_postal_code
from model.validation.util import is_required_column, check_nan_or_falsy


class AgencyJP(Base):
    filename = 'agency_jp.txt'
    __tablename__ = 'agency_jps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    agency_id = Column(String(255), unique=True, nullable=False)
    agency_official_name = Column(String(255))
    agency_zip_number = Column(Integer)
    agency_address = Column(String(255))
    agency_president_pos = Column(String(50))
    agency_president_name = Column(String(10))

    def validate_record(row_series):
        required_columns = ['agency_id']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        postal_code_columns = ['agency_zip_number']
        for column in postal_code_columns:
            if check_nan_or_falsy(row_series, column):
                continue
            postal_code = row_series[column]
            postal_code = zenkaku_to_hankaku(postal_code)
            if not postal_code.isdigit():
                print(f"column {column} is not digit: {postal_code}")
            if postal_code and not is_valid_japanese_postal_code(postal_code):
                print(f"column {column} is not valid postal code: {postal_code}")

        space_separate_columns = ['agency_president_name']
        for column in space_separate_columns:
            if check_nan_or_falsy(row_series, column):
                continue
            name = row_series[column]
            name_split = name.split("　")
            if len(name_split) != 2:
                print(f"column {column} should be space separated: {name}")

        return True, None

    def create_instance_from_series(row_series):
        agency_id = row_series['agency_id']
        agency_official_name = None if check_nan_or_falsy(row_series, 'agency_official_name') else row_series['agency_official_name']
        agency_zip_number = None if check_nan_or_falsy(row_series, 'agency_zip_number') else row_series['agency_zip_number']
        agency_address = None if check_nan_or_falsy(row_series, 'agency_address') else row_series['agency_address']
        agency_president_pos = None if check_nan_or_falsy(row_series, 'agency_president_pos') else row_series['agency_president_pos']
        agency_president_name = None if check_nan_or_falsy(row_series, 'agency_president_name') else row_series['agency_president_name']

        agency_zip_number = int(agency_zip_number) if agency_zip_number else None

        return AgencyJP(
            agency_id=agency_id,
            agency_official_name=agency_official_name,
            agency_zip_number=agency_zip_number,
            agency_address=agency_address,
            agency_president_pos=agency_president_pos,
            agency_president_name=agency_president_name,
        )
