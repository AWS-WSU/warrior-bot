"""CLI Entry point"""

import os

import click

from warrior_bot.core.about import about
from warrior_bot.core.data_handler import JSONHandler
from warrior_bot.core.where import where

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_FILE = "locations.json"
json_handler = JSONHandler(DATA_FILE, DATA_DIR + os.sep)
json_handler.fileExists()


@click.group()
@click.version_option()
def cli() -> None:
    pass


cli.add_command(about)
cli.add_command(where)

if __name__ == "__main__":
    cli()
