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
        self.validate_tables(extract_dir)

        sess = self.new_session()
        try:
            for target_class in self.target_classes:
                target_class.load_table(extract_dir, sess)
            sess.commit()
        except Exception as e:
            sess.rollback()
            raise e

    def validate_tables(self, extract_dir):
        for target_class in self.target_classes:
            target_class.validate_table(extract_dir)

    def check_data(self):
        print("check data")
