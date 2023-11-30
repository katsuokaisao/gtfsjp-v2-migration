import os
import time
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base


class _Base(object):
    @classmethod
    def load_table(cls, extract_dir, sess):
        file_path = os.path.join(extract_dir, cls.filename)
        if not os.path.exists(file_path):
            return

        start_time = time.time()

        df = pd.read_csv(file_path, dtype = 'object')

        batch_size = 10000
        i = 0
        records = []
        for _, row_series in df.iterrows():
            i += 1

            record = cls.create_instance_from_series(row_series)
            records.append(record)

            if i >= batch_size:
                sess.bulk_save_objects(records)

                print("inserted %s records" % len(records))
                i = 0
                records = []

        if len(records) > 0:
            sess.bulk_save_objects(records)
            print("inserted %s records" % len(records))

        process_time = time.time() - start_time
        print("Loaded %s in %s seconds" % (cls.__tablename__, process_time))

    @classmethod
    def validate_table(cls, extract_dir):
        file_path = os.path.join(extract_dir, cls.filename)
        if not os.path.exists(file_path):
            return

        start_time = time.time()

        df = pd.read_csv(file_path, dtype = 'object')

        for _, row_series in df.iterrows():
            valid, reason = cls.validate_record(row_series)
            if not valid:
                print("validation error: %s" % reason)
                print("row series", row_series)
                raise Exception(reason)

        process_time = time.time() - start_time
        print("Validated %s in %s seconds" % (cls.__tablename__, process_time))

    def validate_record(row_series):
        raise("should implement")

    def create_instance_from_series(row_series):
        raise("should implement")

Base = declarative_base(cls=_Base)
