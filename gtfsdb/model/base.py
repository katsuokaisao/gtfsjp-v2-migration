import os
import csv
import time
from sqlalchemy.ext.declarative import declarative_base
from util import UTF8Recorder


class _Base(object):
    @classmethod
    def load_table(self, extract_dir, engine):
        batch_size = 10000
        start_time = time.time()
        file_path = os.path.join(extract_dir, self.filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                utf8_file = UTF8Recorder(f, 'utf-8-sig')
                reader = csv.DictReader(utf8_file)
                reader.fieldnames = [field.strip().lower() for field in reader.fieldnames]

                i = 0
                records = []
                for row in reader:
                    i += 1
                    records.append(row)
                    print(row)

                    if i >= batch_size:
                        # engine.execute(self.__table__.insert(), records)
                        print("inserted %s records" % len(records))
                        i = 0

                if len(records) > 0:
                    # engine.execute(self.__table__.insert(), records)
                    print("inserted %s records" % len(records))

        process_time = time.time() - start_time
        print("Loaded %s in %s seconds" % (self.__tablename__, process_time))

Base = declarative_base(cls=_Base)