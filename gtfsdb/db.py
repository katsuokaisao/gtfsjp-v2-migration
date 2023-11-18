import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database():
    def __init__(self, url):
        self.url = url
        self.engine = None
        self.session_factory = None
        self.target_classes = None
        self.alias = {
            "system_agency_id": {},  # {agency_id: system_agency_id}
            "system_service_id": {}, # {service_id: system_service_id}
            "system_fare_id": {},    # {fare_id: system_fare_id}
            "system_route_id": {},   # {route_id: system_route_id}
            "system_trip_id": {},    # {trip_id: system_trip_id}
            "system_stop_id": {},    # {stop_id: system_stop_id}
            "system_shape_id": {},   # {shape_id: system_shape_id}
            "system_office_id": {},  # {office_id: system_office_id}
        }
        self.debug = False

    def set_target_classes(self, target_classes):
        self.target_classes = target_classes

    def connect(self):
        self.engine = create_engine(self.url)
        self.session_factory = sessionmaker(bind=self.engine)

    def new_session(self):
        return self.session_factory()

    def clean_up(self):
        self.session_factory.close_all()

    def drop_tables(self):
        for target_class in self.target_classes:
            target_class.__table__.drop(self.engine, checkfirst=True)

    def create_tables(self):
        for target_class in self.target_classes:
            target_class.__table__.create(self.engine, checkfirst=True)

    def load_tables(self, extract_dir):
        self.register_alias(extract_dir)

        for target_class in self.target_classes:
            target_class.load_table(extract_dir, self.engine, self.alias)

    def register_alias(self, extract_dir):
        target_alias_params = [
            {
                "necessary_merge": False,
                "file_name": "agency.txt",
                "column_name": "agency_id",
                "alias_name": "system_agency_id",
                "file_name2": "",
                "column_name2": "",
            },
            {
                "necessary_merge": True,
                "file_name": "calendar.txt",
                "column_name": "service_id",
                "alias_name": "system_service_id",
                "file_name2": "calendar_dates.txt",
                "column_name2": "service_id",
            },
            {
                "necessary_merge": True,
                "file_name": "fare_rules.txt",
                "column_name": "fare_id",
                "alias_name": "system_fare_id",
                "file_name2": "fare_attributes.txt",
                "column_name2": "fare_id",
            },
            {
                "necessary_merge": False,
                "file_name": "routes.txt",
                "column_name": "route_id",
                "alias_name": "system_route_id",
                "file_name2": "",
                "column_name2": "",
            },
            {
                "necessary_merge": False,
                "file_name": "trips.txt",
                "column_name": "trip_id",
                "alias_name": "system_trip_id",
                "file_name2": "",
                "column_name2": "",
            },
            {
                "necessary_merge": False,
                "file_name": "stops.txt",
                "column_name": "stop_id",
                "alias_name": "system_stop_id",
                "file_name2": "",
                "column_name2": "",
            },
            {
                "necessary_merge": False,
                "file_name": "shapes.txt",
                "column_name": "shape_id",
                "alias_name": "system_shape_id",
                "file_name2": "",
                "column_name2": "",
            },
            {
                "necessary_merge": False,
                "file_name": "office_jp.txt",
                "column_name": "office_id",
                "alias_name": "system_office_id",
                "file_name2": "",
                "column_name2": "",
            }
        ]

        for param in target_alias_params:
            file_name1 = param["file_name"]
            alias_name = param["alias_name"]
            column_name1 = param["column_name"]
            target_path1 = os.path.join(extract_dir, file_name1)
            if not os.path.exists(target_path1):
                continue

            df1 = pd.read_csv(target_path1, dtype = 'object')
            unique_id = df1[column_name1].unique()

            if param["necessary_merge"]:
                file_name2 = param["file_name2"]
                column_name2 = param["column_name2"]
                target_path2 = os.path.join(extract_dir, file_name2)
                if not os.path.exists(target_path2):
                    continue

                df2 = pd.read_csv(target_path2, dtype = 'object')
                unique_id = np.append(df1[column_name1].unique(), df2[column_name2].unique())

            for system_serial_number, id in enumerate(unique_id):
                self.alias[alias_name][id] = system_serial_number

            if self.debug:
                print(self.alias[alias_name])

    def check_data(self):
        print("check data")
