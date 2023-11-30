from sqlalchemy import Column, Integer, String, Index
from model.base import Base
from model.conversion.string import zenkaku_to_hankaku
from model.validation.util import is_required_column, check_nan_or_falsy


class Transfer(Base):
    filename = 'transfers.txt'
    __tablename__ = 'transfers'
    __table_args__ = (
        Index('idx_transfers_from_stop_id', 'from_stop_id', 'transfer_type'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_stop_id = Column(String(255), nullable=False)
    to_stop_id = Column(String(255), nullable=False)
    system_from_stop_id = Column(Integer, nullable=False)
    system_to_stop_id = Column(Integer, nullable=False)
    transfer_type = Column(Integer, nullable=False) # 0,1,2,3
    min_transfer_time = Column(Integer) # s

    def validate_record(row_series, alias):
        required_columns = ['from_stop_id', 'to_stop_id', 'transfer_type']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        transfer_type = row_series['transfer_type']
        transfer_type = zenkaku_to_hankaku(transfer_type)
        if not transfer_type.isdigit():
            return False, f"column transfer_type should be integer: {transfer_type}"
        if transfer_type not in ['0', '1', '2', '3']:
            return False, f"column transfer_type should be 0, 1, 2, or 3: {transfer_type}"

        if not check_nan_or_falsy(row_series, 'min_transfer_time'):
            min_transfer_time = row_series['min_transfer_time']
            min_transfer_time = zenkaku_to_hankaku(min_transfer_time)
            if not min_transfer_time.isdigit():
                print(f"column min_transfer_time should be digit: {min_transfer_time}")

        return True, None

    def create_instance_from_series(row_series, alias):
        from_stop_id = row_series['from_stop_id']
        to_stop_id = row_series['to_stop_id']
        transfer_type = row_series['transfer_type']
        min_transfer_time = row_series.get('min_transfer_time', None)

        transfer_type = zenkaku_to_hankaku(transfer_type)
        transfer_type = int(transfer_type)

        if min_transfer_time:
            min_transfer_time = zenkaku_to_hankaku(min_transfer_time)
            min_transfer_time = int(min_transfer_time)

        return Transfer(
            from_stop_id=from_stop_id,
            to_stop_id=to_stop_id,
            transfer_type=transfer_type,
            min_transfer_time=min_transfer_time,
        )
