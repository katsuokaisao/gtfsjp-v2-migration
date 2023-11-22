from sqlalchemy import Column, Integer, String, UniqueConstraint
from model.base import Base
from model.conversion.string import zenkaku_to_hankaku


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

    @classmethod
    def validate_record(row_series, alias):
        required_columns = ['trans_id', 'lang', 'translation']
        for column in required_columns:
            if column not in row_series:
                return False, f"column {column} is required"
            if not row_series[column]:
                return False, f"column {column} is required"

        lang_code = ['ja', 'ja-Hrkt', 'en']
        lang = row_series['lang']
        lang = zenkaku_to_hankaku(lang)
        if lang not in lang_code:
            return False, f"column lang should be one of {lang_code}: {row_series['lang']}"

        return True, None

    @classmethod
    def create_instance_from_series(row_series, alias):
        trans_id = row_series['trans_id']
        lang = row_series['lang']
        translation = row_series['translation']

        lang = zenkaku_to_hankaku(lang)

        return Translation(
            trans_id = trans_id,
            lang = lang,
            translation = translation,
        )
