from sqlalchemy import Column, String, Integer, Date
from model.base import Base


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
