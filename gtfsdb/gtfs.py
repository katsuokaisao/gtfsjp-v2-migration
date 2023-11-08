import os
from urllib.request import urlopen
import zipfile
import tempfile


class Gtfs():
    def __init__(self, directory, url, db):
        self.directory = directory
        self.url = url
        self.db = db
        # 必須ファイルのリスト
        self.check_files = [
            "agency.txt",
            "translations.txt",
            "routes.txt",
            "trips.txt",
            "calendar.txt",
            "calendar_dates.txt",
            "stop_times.txt",
            "stops.txt",
        ]

    def load(self):
        if self.url is not None and self.directory is not None:
            raise Exception("Cannot specify both url and directory")

        # zip url が指定されている
        if self.url is not None:
            zip_dir = tempfile.mkdtemp()
            zip_file_path = os.path.join(zip_dir, 'gtfs.zip')
            extract_dir = tempfile.mkdtemp()
            self.download_zip(self.url, zip_file_path)
            self.unzip(zip_file_path, extract_dir)
            self.check_gtfs_files(extract_dir)
            self.db.load_tables(extract_dir)
            return

        # zip directory が指定されている
        # zip ファイルがあればそれを展開してデータをロード
        # zip ファイルがなければ最初から展開されているとみなしてデータをロード
        if self.directory is not None:
            zip_files = [f for f in os.listdir(self.directory) if f.endswith('.zip')]
            if len(zip_files) == 0:
                self.check_gtfs_files(self.directory)
                self.db.load_tables(self.directory)
                return

            if len(zip_files) != 1:
                # 複数ファイルに対応できるようにするか、前処理でファイル統合するかは要検討
                raise Exception("Multiple zip files found")

            zip_file = zip_files[0]
            extract_dir = tempfile.mkdtemp()
            self.unzip(os.path.join(self.directory, zip_file), extract_dir)
            self.check_gtfs_files(extract_dir)
            self.db.load_tables(extract_dir)

    def download_zip(self, url, extract_path):
        with urlopen(url) as download_file:
            data = download_file.read()
            with open(extract_path, mode='wb') as zip_file:
                zip_file.write(data)

    def unzip(self, zip_file_path, extract_dir):
        if not os.path.exists(zip_file_path):
            raise Exception("No zip file found")

        with zipfile.ZipFile(zip_file_path) as obj_zip:
            obj_zip.extractall(extract_dir)

    def check_gtfs_files(self, dir):
        if not os.path.exists(dir):
            raise Exception("No directory found")

        for file in self.check_files:
            if not os.path.exists(os.path.join(dir, file)):
                raise Exception("No file found: " + file)
