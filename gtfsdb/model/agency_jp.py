from sqlalchemy import Column, Integer, String
from model.base import Base
from model.validation.address import is_valid_japanese_postal_code


class AgencyJP(Base):
    filename = 'agency_jp.txt'
    __tablename__ = 'agency_jps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    system_agency_id = Column(Integer, unique=True, nullable=False)
    agency_id = Column(String(255), unique=True, nullable=False)
    agency_official_name = Column(String(255))
    agency_zip_number = Column(Integer)
    agency_address = Column(String(255))
    agency_president_pos = Column(String(50))
    agency_president_name = Column(String(10))

    def validate_record(self, row_series, alias):
        required_columns = ['agency_id']
        for column in required_columns:
            if column not in row_series:
                return False, f"column {column} is required"
            if not row_series[column]:
                return False, f"column {column} is required"

        postal_code_columns = ['agency_zip_number']
        for column in postal_code_columns:
            if column in row_series:
                postal_code = row_series[column]
                if postal_code and not is_valid_japanese_postal_code(postal_code):
                    print(f"column {column} is not valid postal code: {postal_code}")

        space_separate_columns = ['agency_president_name']
        for column in space_separate_columns:
            if column in row_series:
                name = row_series[column]
                name_split = name.split("　")
                if len(name_split) != 2:
                    print(f"column {column} should not contain zenkaku space: {name}")

        return True, None

    @classmethod
    def create_instance_from_series(row_series, alias):
        agency_id = row_series['agency_id']
        agency_official_name = row_series.get('agency_official_name', None)
        agency_zip_number = row_series.get('agency_zip_number', None)
        agency_address = row_series.get('agency_address', None)
        agency_president_pos = row_series.get('agency_president_pos', None)
        agency_president_name = row_series.get('agency_president_name', None)

        agency_zip_number = int(agency_zip_number) if agency_zip_number else None

        system_agency_id = alias['system_agency_id'].get(agency_id, None)

        return AgencyJP(
            system_agency_id=system_agency_id,
            agency_id=agency_id,
            agency_official_name=agency_official_name,
            agency_zip_number=agency_zip_number,
            agency_address=agency_address,
            agency_president_pos=agency_president_pos,
            agency_president_name=agency_president_name,
        )
