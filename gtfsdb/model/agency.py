from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from model.base import Base
from model.validation.url import is_valid_url
from model.validation.tz import is_valid_timezone
from model.validation.lang import is_valid_language_code
from model.validation.phone import is_valid_landline_phone
from model.validation.email import is_valid_email
from model.conversion.string import zenkaku_to_hankaku

class Agency(Base):
    filename = 'agency.txt'
    system_alias_name = "system_agency_id"
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

    def validate_record(self, row_series, alias):
        required_columns = ['agency_id', 'agency_name', 'agency_url', 'agency_timezone']
        for column in required_columns:
            if column not in row_series:
                return False, f"column {column} is required"
            if not row_series[column]:
                return False, f"column {column} is required"

        # agency_url HPがない場合は、その旨が記載されるらしい。。。
        url_columns = ['agency_url', 'agency_fare_url']
        for column in url_columns:
            if column in row_series:
                url = row_series[column]
                if not is_valid_url(url):
                    print(f"column {column} is not valid url: {url}")

        timezone_columns = ['agency_timezone']
        for column in timezone_columns:
            if column in row_series:
                timezone = row_series[column]
                timezone = timezone.strip()
                timezone = zenkaku_to_hankaku(timezone)
                if not is_valid_timezone(timezone):
                    return False, f"column {column} is not valid timezone: {timezone}"

        # 必須カラムではないので、間違っていてもデバッグログに出力するだけ
        lang_code_columns = ['agency_lang']
        for column in lang_code_columns:
            if column in row_series:
                lang_code = row_series[column]
                lang_code = lang_code.strip()
                if lang_code:
                    lang_code = zenkaku_to_hankaku(lang_code)
                    if not is_valid_language_code(lang_code):
                        print(f"column {column} is not valid language code: {lang_code}")

        phone_columns = ['agency_phone']
        for column in phone_columns:
            if column in row_series:
                phone = row_series[column]
                phone = phone.strip()
                if phone:
                    phone = zenkaku_to_hankaku(phone)
                    if not is_valid_landline_phone(phone):
                        print(f"column {column} is not valid phone: {phone}")

        email_columns = ['agency_email']
        for column in email_columns:
            if column in row_series:
                email = row_series[column]
                email = email.strip()
                if email:
                    email = zenkaku_to_hankaku(email)
                    if not is_valid_email(email):
                        print(f"column {column} is not valid email: {email}")

        return True, ""

    def make_record(self, row_series, alias):
        self.agency_id = row_series['agency_id']
        self.agency_name = row_series['agency_name']
        self.agency_url = row_series['agency_url']
        self.agency_timezone = row_series['agency_timezone']
        self.agency_lang = row_series['agency_lang']
        self.agency_phone = row_series['agency_phone']
        self.agency_fare_url = row_series['agency_fare_url']
        self.agency_email = row_series['agency_email']

    def make_dict(self):
        return {
            'agency_id': self.agency_id,
            'agency_name': self.agency_name,
            'agency_url': self.agency_url,
            'agency_timezone': self.agency_timezone,
            'agency_lang': self.agency_lang,
            'agency_phone': self.agency_phone,
            'agency_fare_url': self.agency_fare_url,
            'agency_email': self.agency_email,
        }