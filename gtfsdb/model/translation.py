from sqlalchemy import Column, Integer, String, UniqueConstraint
from model.base import Base


class Translation(Base):
    filename = 'translations.txt'
    __tablename__ = 'translations'
    __table_args__ = (
        UniqueConstraint('trans_id', 'lang', name='unique_trans_id_and_lang'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    trans_id = Column(String(255), index=True, nullable=False)
    lang = Column(String(10), nullable=False)
    translation = Column(String(255), nullable=False)
