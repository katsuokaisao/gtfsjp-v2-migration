import os
import time
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert


class _Base(object):
    @classmethod
    def load_table(self, extract_dir, engine, alias):
        file_path = os.path.join(extract_dir, self.filename)
        if not os.path.exists(file_path):
            return

        start_time = time.time()

        df = pd.read_csv(file_path)

        # validation check
        for _, row_series in df.iterrows():
            valid, reason = self.validate_record(row_series, alias)
            if not valid:
                print("validation error: %s" % reason)
                print("row series", row_series)
                raise Exception(reason)

        batch_size = 10000
        i = 0
        records = []
        for _, row_series in df.iterrows():
            i += 1

            format_record = self.make_record(row_series, alias)
            records.append(format_record)

            if i >= batch_size:
                # e.g.
                # ...     insert(User),
                # ...     [
                # ...         {"name": "spongebob", "fullname": "Spongebob Squarepants"},
                # ...         {"name": "sandy", "fullname": "Sandy Cheeks"},
                # ...         {"name": "patrick", "fullname": "Patrick Star"},
                # ...         {"name": "squidward", "fullname": "Squidward Tentacles"},
                # ...         {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
                # ...     ],
                # ... )
                engine.execute(
                    insert(
                        self.__class__,
                        records
                    )
                )
                print("inserted %s records" % len(records))
                i = 0
                records = []

        if len(records) > 0:
            engine.execute(
                insert(
                    self.__class__,
                    records
                )
            )
            print("inserted %s records" % len(records))

        process_time = time.time() - start_time
        print("Loaded %s in %s seconds" % (self.__tablename__, process_time))

    def validate_record(row_series, alias):
        raise("should implement")

    def make_record(row_series, alias):
        raise("should implement")

Base = declarative_base(cls=_Base)