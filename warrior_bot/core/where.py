import os

import click

from warrior_bot.core.data_handler import DataHandler

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@click.command()
@click.argument("loc_query", nargs=-1)
def where(loc_query: tuple[str, ...]) -> None:
    """Find POI's around campus."""
    if not loc_query:
        click.echo("Please specify a location.")
        return

    handler = DataHandler(DATA_DIR, "locations.json")
    result = handler.search(" ".join(loc_query))
    click.echo(result if result else "No documented match found.")
