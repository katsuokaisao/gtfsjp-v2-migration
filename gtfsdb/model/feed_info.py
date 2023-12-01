import datetime
from sqlalchemy import Column, String, Integer, Date
from model.base import Base
from model.validation.url import is_valid_url
from model.validation.lang import is_valid_language_code
from model.validation.time import is_valid_yyyymmdd_format
from model.conversion.string import zenkaku_to_hankaku
from model.validation.util import is_required_column, check_nan_or_falsy

class FeedInfo(Base):
    filename = 'feed_info.txt'
    __tablename__ = 'feed_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    feed_publisher_name = Column(String(255), index=True, nullable=False)
    feed_publisher_url = Column(String(255), nullable=False)
    feed_lang = Column(String(10), nullable=False) # ja
    feed_start_date = Column(Date) # YYYYMMDD
    feed_end_date = Column(Date) # YYYYMMDD
    feed_version = Column(String(255))

    def validate_record(row_series):
        required_columns = ['feed_publisher_name', 'feed_publisher_url', 'feed_lang']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        url_columns = ['feed_publisher_url']
        for column in url_columns:
            url = row_series[column]
            if not is_valid_url(url):
                return False, f"column {column} is not valid url: {url}"

        lang_code_columns = ['feed_lang']
        for column in lang_code_columns:
            lang_code = row_series[column]
            lang_code =zenkaku_to_hankaku(lang_code)
            if not is_valid_language_code(lang_code):
                return False, f"column {column} is not valid language code: {lang_code}"

        yyyymmdd_format_columns = ['feed_start_date', 'feed_end_date']
        for column in yyyymmdd_format_columns:
            if check_nan_or_falsy(row_series, column):
                continue
            date = row_series[column]
            date = zenkaku_to_hankaku(date)
            if not is_valid_yyyymmdd_format(date):
                return False, f"column {column} is not valid yyyymmdd format: {date}"

        if 'feed_start_date' in row_series and 'feed_end_date' in row_series:
            feed_start_date = row_series['feed_start_date']
            feed_end_date = row_series['feed_end_date']
            if feed_start_date and feed_end_date:
                feed_start_date = zenkaku_to_hankaku(feed_start_date)
                feed_end_date = zenkaku_to_hankaku(feed_end_date)
                feed_start_date = datetime.datetime.strptime(feed_start_date, '%Y%m%d')
                feed_end_date = datetime.datetime.strptime(feed_end_date, '%Y%m%d')
                if feed_start_date > feed_end_date:
                    print(f"column feed_start_date should be earlier than feed_end_date: {feed_start_date} > {feed_end_date}")

        return True, None

    def create_instance_from_series(row_series):
        feed_publisher_name = row_series['feed_publisher_name']
        feed_publisher_url = row_series['feed_publisher_url']
        feed_lang = row_series['feed_lang']
        feed_start_date = None if check_nan_or_falsy(row_series, 'feed_start_date') else row_series['feed_start_date']
        feed_end_date = None if check_nan_or_falsy(row_series, 'feed_end_date') else row_series['feed_end_date']
        feed_version = None if check_nan_or_falsy(row_series, 'feed_version') else row_series['feed_version']

        feed_lang = zenkaku_to_hankaku(feed_lang)
        if feed_start_date:
            feed_start_date = zenkaku_to_hankaku(feed_start_date)
            feed_start_date = datetime.datetime.strptime(feed_start_date, '%Y%m%d')
        if feed_end_date:
            feed_end_date = zenkaku_to_hankaku(feed_end_date)
            feed_end_date = datetime.datetime.strptime(feed_end_date, '%Y%m%d')

        return FeedInfo(
            feed_publisher_name=feed_publisher_name,
            feed_publisher_url=feed_publisher_url,
            feed_lang=feed_lang,
            feed_start_date=feed_start_date,
            feed_end_date=feed_end_date,
            feed_version=feed_version,
        )
