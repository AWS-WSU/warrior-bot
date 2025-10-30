"""CLI Entry point"""

import click

from core.about import about
from core.where import where


@click.group()
@click.version_option()
def cli():
    pass


cli.add_command(about)
cli.add_command(where)

if __name__ == "__main__":
    cli()
