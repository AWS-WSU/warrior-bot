"""
Command to refresh/sync data parsing for any given service
"""

import importlib.metadata
from typing import Any, Callable

import click

from warrior_bot.utils.faculty_parser import build_faculty_cache

warrior_bot_version = importlib.metadata.version("warrior-bot")


def _get_version(*sub: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Retrieve the current version of warrior-bot
    """

    def dec(obj: Callable[..., Any]) -> Callable[..., Any]:
        doc = obj.__doc__ or ""
        obj.__doc__ = doc.format(*sub)
        return obj

    return dec


@click.command()
@click.argument("service", nargs=-1)
@_get_version(warrior_bot_version)
def sync(service: str) -> None:
    """
    Manually refresh data parsing services\n
    warrior-bot version: {0} currently handles the following services:\n
        staff:\n
          - Parses https://bulletins.wayne.edu/faculty/
    """
    text = " ".join(service).strip()
    if not text:
        click.echo(
            click.style(
                "Please provide a valid warrior-bot service to reresh.\n"
                "Run wb sync --help for a list of services",
                fg="red",
            )
        )
        return

    target = service[0].strip().lower()

    if target == "staff":
        build_faculty_cache()
        click.echo(click.style("Staff cache has been successfully built!", fg="green"))
        return

    click.echo(
        click.style(
            f"Unknown service: {target}",
            fg="red",
        )
    )
