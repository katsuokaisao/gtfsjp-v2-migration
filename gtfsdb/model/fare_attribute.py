from sqlalchemy import Column, String, Integer, SmallInteger
from model.base import Base
from model.conversion.string import zenkaku_to_hankaku
from model.validation.currency import is_valid_currency_code
from model.validation.util import is_required_column, check_nan_or_falsy

class FareAttribute(Base):
    filename = 'fare_attributes.txt'
    __tablename__ = 'fare_attributes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fare_id = Column(String(255), index=True, nullable=False)
    price = Column(Integer, nullable=False)
    currency_type = Column(String(10), nullable=False) # JPY
    payment_method = Column(SmallInteger, nullable=False) # 0,1
    transfers = Column(SmallInteger, nullable=False) # 0,1,2,3(空白)
    transfer_duration = Column(Integer)

    def validate_record(row_series):
        required_columns = ['fare_id', 'price', 'currency_type', 'payment_method', 'transfers']
        for column in required_columns:
            if not is_required_column(row_series, column):
                return False, f"column {column} is required"

        price = row_series['price']
        price = zenkaku_to_hankaku(price)
        if not price.isdigit():
            return False, f"column price should be integer"
        price = int(price)
        if price < 0:
            return False, f"column price should be positive integer"

        currency_type = row_series['currency_type']
        currency_type = zenkaku_to_hankaku(currency_type)
        if not is_valid_currency_code(currency_type):
            return False, f"column currency_type should be valid currency code: {currency_type}"

        payment_method = row_series['payment_method']
        payment_method = zenkaku_to_hankaku(payment_method)
        if payment_method not in ['0', '1']:
            return False, f"column payment_method should be 0 or 1"

        transfers = row_series['transfers']
        transfers = zenkaku_to_hankaku(transfers)
        if transfers not in ['0', '1', '2', '']:
            return False, f"column transfers should be 0, 1, 2, or empty string"

        if not check_nan_or_falsy(row_series, 'transfer_duration'):
            transfer_duration = row_series['transfer_duration']
            transfer_duration = zenkaku_to_hankaku(transfer_duration)
            if not transfer_duration.isdigit():
                print(f"column transfer_duration should be integer: {transfer_duration}")
            transfer_duration = int(transfer_duration)
            if transfer_duration < 0:
                print(f"column transfer_duration should be positive integer: {transfer_duration}")

        return True, None

    def create_instance_from_series(row_series):
        fare_id = row_series['fare_id']
        price = row_series['price']
        currency_type = row_series['currency_type']
        payment_method = row_series['payment_method']
        transfers = row_series['transfers']
        transfer_duration = None if check_nan_or_falsy(row_series, 'transfer_duration') else row_series['transfer_duration']

        price = zenkaku_to_hankaku(price)
        price = int(price)

        currency_type = zenkaku_to_hankaku(currency_type)

        payment_method = zenkaku_to_hankaku(payment_method)
        payment_method = int(payment_method)

        transfers = zenkaku_to_hankaku(transfers)
        if transfers == '':
            transfers = 3
        else:
            transfers = int(transfers)

        if transfer_duration:
            transfer_duration = zenkaku_to_hankaku(transfer_duration)
            transfer_duration = int(transfer_duration)

        return FareAttribute(
            fare_id=fare_id,
            price=price,
            currency_type=currency_type,
            payment_method=payment_method,
            transfers=transfers,
            transfer_duration=transfer_duration,
        )
