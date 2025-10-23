"""Command-line interface for Warrior Bot."""

import click


@click.command()
@click.argument('query', nargs=-1, required=False)
@click.version_option()
def main(query):
    """Warrior Bot - Your Wayne State University terminal assistant."""
    if query:
        question = ' '.join(query)
        click.echo(f"You asked: {question}")
    else:
        click.echo("Warrior Bot ready. Try: warrior-bot <your question>")


if __name__ == '__main__':
    main()

