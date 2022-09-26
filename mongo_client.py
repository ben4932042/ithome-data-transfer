# pylint: disable=no-value-for-parameter
"""mongo client cli"""
import os
import re
import click
import pymongo
import pandas as pd


def _clean_data(text: str) -> str:
    return re.sub('\t|\r|\n|\u3000|,|\xa0', '。', text)

def _clean_df(data: pd.DataFrame) -> pd.DataFrame:
    for _col in data.select_dtypes(include=['object']).columns:
        data[_col] = data[_col].map(_clean_data)
    return data

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

    def dump_to_file(self, skip_column: set, file_path: str) -> None:
        """get mongo data and output to csv
        Note: for demo usage, data will replace special characters to space"""
        _clean_df(self.get_mongo_data(skip_column=skip_column)).to_csv(file_path, index=None)

    def check_data_count(self, contain_header: bool = True) -> int:
        """get mongo data count"""
        data_count = 1 if contain_header else 0
        return self.collection.count_documents({}) + data_count

    def truncate_mongo_data(self) -> None:
        """drop mongo collection"""
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
@click.option('--csv-file-path', '-file')
def to_csv(ctx, skip_column: set, csv_file_path: str):
    """get crawl data"""
    ctx.obj['mongo_client'].dump_to_file(skip_column=skip_column, file_path=csv_file_path)

@cli.command()
@click.pass_context
def housekeeping(ctx):
    """clean crawl data"""
    ctx.obj['mongo_client'].truncate_mongo_data()


if __name__ == "__main__":
    cli()