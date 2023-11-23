import click
from db import Database
from gtfs import Gtfs
from model_class import target_classes


@click.group()
def cli():
    pass

@cli.command(short_help='test connection to database')
@click.option('--database_url', '-db', help='postgresql database url with appropriate permissions for connection')
def test_connection(database_url):
    db = Database(database_url)
    db.connect()
    print("connected")

@cli.command(short_help='create table')
@click.option('--database_url', '-db', help='postgresql database url with appropriate permissions for connection')
@click.option("--drop", "-d", is_flag=False, help="drop tables before creating")
def create_table(database_url, drop):
    db = Database(database_url)
    db.connect()
    db.set_target_classes(target_classes)
    if drop:
        db.drop_tables()
    db.create_tables()

@cli.command(short_help='parse csv files and insert into tables')
@click.option('--database_url', '-db', help='postgresql database url with appropriate permissions for connection')
@click.option('--directory', '-dir', help='directory containing gtfs csv files or zip file')
@click.option('--url', '-u', help='url containing GTFS zip file')
def migrate(database_url, directory, url):
    db = Database(database_url)
    db.connect()
    db.set_target_classes(target_classes)
    gtfs = Gtfs(directory, url, db)
    gtfs.load()

@cli.command(short_help='validate csv files')
@click.option('--database_url', '-db', help='postgresql database url with appropriate permissions for connection')
@click.option('--directory', '-dir', help='directory containing gtfs csv files or zip file')
@click.option('--url', '-u', help='url containing GTFS zip file')
def validate(database_url, directory, url):
    db = Database(database_url)
    db.connect()
    db.set_target_classes(target_classes)
    gtfs = Gtfs(directory, url, db)
    gtfs.validate()

@cli.command(short_help='check data exists in tables')
@click.option('--database_url', '-db', help='postgresql database url with appropriate permissions for connection')
def check_data(database_url):
    db = Database(database_url)
    db.connect()
    db.check_data()
    print("check ok")

if __name__ == '__main__':
    cli()