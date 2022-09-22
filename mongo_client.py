# pylint: disable=no-value-for-parameter
"""mongo client cli"""
import os
import click
import pymongo
import pandas as pd

class IthomeMongoClient:
    """ithome mongo interface"""
    def __init__(self, collection: str):
        mongo_client = pymongo.MongoClient(os.getenv("MONGO_HOST", "mongodb://localhost:27017/"))
        mongo_db = mongo_client[os.getenv("MONGO_DB", "ithome_ironman")]
        self.collection = mongo_db[collection]

    def get_mongo_data(self, skip_column: set) -> pd.DataFrame:
        """get mongo data to dataframe"""
        mongo_df = pd.DataFrame(list(self.collection.find()))
        return mongo_df[[_col for _col in mongo_df.columns if not _col in skip_column]]

    def dump_to_csv(self, skip_column: set, csv_file_path: str) -> None:
        """get mongo data and output to csv"""
        self.get_mongo_data(skip_column=skip_column).to_csv(csv_file_path, index=None)

    def check_data_count(self, contain_header: bool = True) -> int:
        """get data count in mongo"""
        data_count = 1 if contain_header else 0
        return self.collection.count_documents({}) + data_count

    def truncate_mongo_data(self) -> None:
        """drop mongo collection data"""
        self.collection.drop()

@click.group()
@click.option("--collection", "-c", required=True, type=str)
@click.pass_context
def cli(ctx, collection: str):
    """entrypoint"""
    ctx.ensure_object(dict)
    ctx.obj['mongo_client'] = IthomeMongoClient(collection=collection)

@cli.command()
@click.pass_context
@click.option('--contain-header', is_flag=True)
def count_data(ctx, contain_header: bool = True):
    """count crawl data in mongo, verify usage."""
    click.echo(ctx.obj['mongo_client'].check_data_count(contain_header))

@cli.command()
@click.pass_context
@click.option('--skip-column', '-s',  multiple=True)
@click.option('-csv-file-path', '-csv')
def to_csv(ctx, skip_column: set, csv_file_path: str):
    """get crawl data"""
    ctx.obj['mongo_client'].dump_to_csv(skip_column=skip_column, csv_file_path=csv_file_path)

@cli.command()
@click.pass_context
def housekeeping(ctx):
    """clean crawl data"""
    ctx.obj['mongo_client'].truncate_mongo_data()


if __name__ == "__main__":
    cli()
