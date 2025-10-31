import difflib
import json
import os

import click


class JSONHandler:
    """
    general plan
    https://www.massinteract.com/wayne-state-university/#24469625p&259.59h&99.76t

    student center
        food
            panda-express
            taco bell
            ...
        midtown market
        game room
            pool tables
            ping pong tables
            gaming center
    recreation and fitness center
    UGL - Undergraduate Library
        Study Spaces
        Reservable Meeting Rooms
            go by floor?
        honors college
    Purdy Kresge Library
    STEM Innovation Learning Center
    Old Main
        Planetarium
        Schaver Music Hall
        Gordon L. Grosscup Anthropolgoy Museum
    welcome center
    on-campus living
        Towers Residential Suites
        Anthony Wayne Drive Apartments
            definitely more, might be some popular "unofficial" apartments too
    Schapp Chemistry Building and Lecture Hall
    """

    def __init__(self, jsonFileName, jsonFilePath):
        self.fileName = jsonFileName
        self.filePath = jsonFilePath

    def fileExists(self, createIfNotExists: bool = True) -> bool:
        """
        Check if JSON data file exists already, calls createFile if not

        Parameters:
            createIfNotExists (bool, default = True):
                create a JSON file automatically if
                one is found to not exist

        Returns:
            bool: True if file exists, False if not
        """

        if os.path.exists(self.filePath + self.fileName):
            return True
        else:
            if not createIfNotExists:
                return False
            else:
                if self.createFile(self.fileName):
                    return False
                else:
                    raise Exception

    def createFile(self, newFileName: str = "data.json") -> bool:
        """
        Creates empty JSON file, will be called from
        fileExists in most cases

        Parameters:
            filename (str, default = "data.json"):
                name of the file to create with file
                extension

        Returns:
            bool: True if success, raises Exception if failure
        """

        try:
            with open(newFileName, "w") as writeFile:
                json.dump({}, writeFile, indent=4)

            return True
        except Exception as e:
            raise Exception from e


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
    matches = difflib.get_close_matches(query, LOCATIONS.keys(), n=1, cutoff=0.6)

    if matches:
        location = matches[0]
        click.echo(LOCATIONS[location])
    else:
        click.echo("No documented match found.")
