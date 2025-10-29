import difflib

import click

# placeholder to test fuzzy matching
# ideally here we'd actually just pull from a .json file or something similar
LOCATIONS = {
    "panda express": "Panda express is located in the Student Center",
    "library": "UGL is across the Student Center",
}


@click.command()
@click.argument("loc_query", nargs=-1)
def where(loc_query):
    """Find POI's around campus."""
    if not loc_query:
        click.echo("Please specify a location.")

    query = " ".join(loc_query).lower().strip()
    matches = difflib.get_close_matches(
        query, LOCATIONS.keys(), n=1, cutoff=0.6
    )

    if matches:
        location = matches[0]
        click.echo(LOCATIONS[location])
    else:
        click.echo("No documented match found.")
