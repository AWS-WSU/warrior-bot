import difflib
import json
import os
from typing import cast


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

    def __init__(self, jsonFileName: str, jsonFilePath: str):
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


class DataHandler:
    flat: dict[str, str]
    data: dict[str, object]
    path: str

    def __init__(self, data_dir: str, filename: str) -> None:
        self.path = os.path.join(data_dir, filename)
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Missing data file: {self.path}")
        with open(self.path, "r") as f:
            self.data = json.load(f)
        self.flat = self._flatten(self.data)

    def _flatten(self, d: dict[str, object], parent_key: str = "") -> dict[str, str]:
        items: dict[str, str] = {}
        for k, v in d.items():
            new_key = f"{parent_key} {k}".strip()
            if isinstance(v, dict):
                v_dict = cast(dict[str, object], v)
                if "__description__" in v_dict:
                    items[new_key] = str(v_dict["__description__"])
                items.update(self._flatten(v_dict, new_key))
            else:
                items[new_key] = str(v)
        return items

    def search(self, query: str) -> str | None:
        query = query.lower().strip()
        matches = difflib.get_close_matches(query, self.flat.keys(), n=1, cutoff=0.6)
        return self.flat[matches[0]] if matches else None
