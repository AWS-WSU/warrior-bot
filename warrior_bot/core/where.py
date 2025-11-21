"""
warrior-bot's 'where' command module.

Commands:
- where [query]: Find POI's around campus or staff member details.

"""

import os

import click

from warrior_bot.core.data_handler import DataHandler
from warrior_bot.utils.extract_staff import StaffExtractor

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@click.command()
@click.argument("query", nargs=-1)
def where(query: str) -> None:
    """Find POI's around campus."""
    text = " ".join(query).strip()
    if not text:
        click.echo("Please provide a valid person or place to search for.")
        return

    extractor = StaffExtractor()
    staff_lst = extractor.resolve_user_input_to_name_and_id(text)
    selected = None
    if len(staff_lst) > 1:
        click.echo(click.style("Multiple matches found:", fg="yellow"))
        for i, (staff_name, staff_id) in enumerate(staff_lst, 1):
            click.echo(f"{i}. {extractor.normalize_name(staff_name)} ({staff_id})")
        
        while True:
            choice = click.prompt(
                "Enter a number to select a staff member, or type 'no' or enter nothing to cancel",
                default="no"
            ).strip().lower()

            if choice == "no":
                click.echo("Search cancelled.")
                return None

            # Must be a valid number
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(staff_lst):
                    n = staff_lst[idx - 1]
                    break

            click.echo("Invalid choice, please try again.")
    elif (len(staff_lst) > 0):
        selected = staff_lst[0]

    if selected:
        staff_name, staff_id = selected

        proper = extractor.normalize_name(staff_name)
        dep: str | None = extractor.resolve_id_to_department(staff_id)
        office: str | None = extractor.resolve_id_to_office(staff_id)
        email: str | None = extractor.resolve_id_to_email(staff_id)
        phone: str | None = extractor.resolve_id_to_phone(staff_id)

        if not any([dep, office, email, phone]):
            click.echo(
                click.style(
                    "[ERROR] No documented information found for this staff member.\n"
                    "This is probably a student or an incomplete profile.",
                    fg="red",
                )
            )
            return

        if dep:
            click.echo(
                click.style("", fg="green")
                + click.style(proper, fg="blue")
                + click.style(" works in the ", fg="green")
                + click.style(dep, fg="blue")
                + click.style(" department", fg="green")
            )
        else:
            click.echo(
                click.style(
                    "[ERROR] Department could not be found for this staff member.",
                    fg="red",
                )
            )

        if office:
            click.echo(
                click.style("You can find them at ", fg="green")
                + click.style(office, fg="blue")
            )
        else:
            click.echo(
                click.style(
                    "[ERROR] This staff member does not have a registered office.",
                    fg="red",
                )
            )

        if email:
            click.echo(
                click.style("Their email is ", fg="green")
                + click.style(email, fg="blue")
            )
        else:
            click.echo(
                click.style(
                    "[ERROR] This staff member does not have a registered email.",
                    fg="red",
                )
            )

        if phone:
            click.echo(
                click.style("and their office phone number is ", fg="green")
                + click.style(phone, fg="blue")
            )
        else:
            click.echo(
                click.style(
                    "[ERROR] This staff member does not have\n"
                    "a registered phone number.",
                    fg="red",
                )
            )

        return

    handler = DataHandler(DATA_DIR, "locations.json")
    result = handler.search(text)
    click.echo(result if result else "No documented match found.")