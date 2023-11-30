from sqlalchemy import Column, String, Integer
from model.base import Base
from model.validation.url import is_valid_url
from model.validation.phone import is_valid_landline_phone
from model.conversion.string import zenkaku_to_hankaku
from model.validation.util import is_required_column, check_nan_or_falsy


class OfficeJP(Base):
    filename = 'office_jp.txt'
    __tablename__ = 'office_jps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    office_id = Column(String(255), index=True, nullable=False)
    office_name = Column(String(255), nullable=False)
    office_url = Column(String(255))
    office_phone = Column(String(50))

    def validate_record(row_series):
        required_columns = ['office_id', 'office_name']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        url_columns = ['office_url']
        for column in url_columns:
            if check_nan_or_falsy(row_series, column):
                continue
            url = row_series[column]
            url = zenkaku_to_hankaku(url)
            if not is_valid_url(url):
                print(f"column {column} is not valid url: {url}")

        phone_columns = ['office_phone']
        for column in phone_columns:
            if check_nan_or_falsy(row_series, column):
                continue
            phone = row_series[column]
            phone = zenkaku_to_hankaku(phone)
            if not is_valid_landline_phone(phone):
                print(f"column {column} should be landline phone number: {phone}")

        return True, None

    def create_instance_from_series(row_series):
        office_id = row_series['office_id']
        office_name = row_series['office_name']
        office_url = row_series.get('office_url', None)
        office_phone = row_series.get('office_phone', None)

        office_url = zenkaku_to_hankaku(office_url)
        office_phone = zenkaku_to_hankaku(office_phone)

        return OfficeJP(
            office_id=office_id,
            office_name=office_name,
            office_url=office_url,
            office_phone=office_phone
        )
