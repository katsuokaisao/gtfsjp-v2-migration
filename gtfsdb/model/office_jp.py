from sqlalchemy import Column, String, Integer
from model.base import Base
from model.validation.url import is_valid_url
from model.validation.phone import is_valid_landline_phone
from model.conversion.string import zenkaku_to_hankaku


class OfficeJP(Base):
    filename = 'office_jp.txt'
    __tablename__ = 'office_jps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    office_id = Column(String(255), index=True, nullable=False)
    office_name = Column(String(255), nullable=False)
    office_url = Column(String(255))
    office_phone = Column(String(50))

    @classmethod
    def validate_record(row_series, alias):
        required_columns = ['office_id', 'office_name']
        for column in required_columns:
            if column not in row_series:
                return False, f"column {column} is required"
            if not row_series[column]:
                return False, f"column {column} is required"

        url_columns = ['office_url']
        for column in url_columns:
            if column in row_series:
                url = row_series[column]
                if url:
                    url = zenkaku_to_hankaku(url)
                    if not is_valid_url(url):
                        print(f"column {column} should be url: {url}")

        phone_columns = ['office_phone']
        for column in phone_columns:
            if column in row_series:
                phone = row_series[column]
                if phone:
                    phone = zenkaku_to_hankaku(phone)
                    if not is_valid_landline_phone(phone):
                        print(f"column {column} should be landline phone number: {phone}")

        return True, None

    @classmethod
    def create_instance_from_series(row_series, alias):
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
