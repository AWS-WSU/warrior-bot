import difflib
import json
import os
import re
from typing import Mapping, cast


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
        Creates empty JSON file, will be called from fileExists in most cases
        """
        try:
            with open(newFileName, "w") as writeFile:
                json.dump({}, writeFile, indent=4)
            return True
        except Exception as e:
            raise Exception from e


class DataHandler:
    flat: dict[str, str]
    data: Mapping[str, object]
    path: str

    def __init__(self, data_dir: str, filename: str) -> None:
        self.path = os.path.join(data_dir, filename)
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Missing data file: {self.path}")
        with open(self.path, "r") as f:
            self.data = json.load(f)
        self.flat = self._flatten(self.data)

    def _flatten(self, d: Mapping[str, object], parent_key: str = "") -> dict[str, str]:
        items: dict[str, str] = {}
        for k, v in d.items():
            new_key = f"{parent_key} {k}".strip()
            if isinstance(v, dict):
                v_dict = cast(dict[str, object], v)
                if "__description__" in v_dict:
                    items[new_key] = str(v_dict["__description__"])
                items.update(self._flatten(v_dict, new_key))
            elif isinstance(v, list):
                # Handle arrays of objects (e.g., buildings, locations)
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        item_dict = cast(dict[str, object], item)
                        result_value = ""

                        # Handle nested "details" dicts first
                        if "details" in item_dict and isinstance(
                            item_dict["details"], dict
                        ):
                            details = item_dict["details"]
                            for dk, dv in details.items():
                                if isinstance(dv, dict):
                                    for subk, subv in dv.items():
                                        items[f"{new_key} {subk}"] = str(subv)
                                        items[subk] = str(subv)
                                else:
                                    items[f"{new_key} {dk}"] = str(dv)
                                    items[dk] = str(dv)

                        # Build result_value prioritizing address with name for context
                        if "address" in item_dict and "name" in item_dict:
                            result_value = (
                                f"{item_dict['name']} - {item_dict['address']}"
                            )
                        elif "address" in item_dict:
                            result_value = str(item_dict["address"])
                        elif "description" in item_dict:
                            result_value = str(item_dict["description"])
                        elif "name" in item_dict:
                            result_value = str(item_dict["name"])
                        else:
                            result_value = (
                                str(self.data["contact"]["campus_map"])
                                if "contact" in self.data
                                and isinstance(self.data["contact"], dict)
                                and "campus_map" in self.data["contact"]
                                else "https://maps.wayne.edu"
                            )

                        # Extract searchable fields
                        searchable_fields = [
                            "name",
                            "code",
                            "address",
                            "description",
                            "type",
                        ]
                        for field in searchable_fields:
                            if field in item_dict:
                                field_key = f"{new_key} {field} {i}"
                                field_value = str(item_dict[field])
                                items[field_key] = result_value
                                items[field_value] = result_value
            else:
                items[new_key] = str(v)
        return items

    def search(self, query: str) -> str | None:
        query = query.lower().replace("_", " ").strip()
        normalized = {k.lower().replace("_", " "): k for k in self.flat.keys()}

        # exact key or value match first
        if query in normalized:
            return self.flat[normalized[query]]
        for nk, orig in normalized.items():
            if query == nk.split()[-1]:
                return self.flat[orig]

        # substring match with word-boundary awareness
        # prioritize keys where query appears with word boundaries
        pattern = r"\b" + re.escape(query) + r"\b"
        word_bound_keys = [
            (nk, orig) for nk, orig in normalized.items() if re.search(pattern, nk)
        ]
        if word_bound_keys:
            # Filter out keys with "/" to avoid "Faculty/Administration" issues
            no_slash = [x for x in word_bound_keys if "/" not in x[1]]
            if no_slash:
                best_match = min(no_slash, key=lambda x: len(x[0]))
                return self.flat[best_match[1]]
            # If all have slashes, use shortest
            best_match = min(word_bound_keys, key=lambda x: len(x[0]))
            return self.flat[best_match[1]]

        # general substring match with shortest key
        substring_matches = [
            (nk, orig) for nk, orig in normalized.items() if query in nk
        ]
        if substring_matches:
            best_match = min(substring_matches, key=lambda x: len(x[0]))
            return self.flat[best_match[1]]

        # higher cut off for fuzzy match to reduce noise
        matches = difflib.get_close_matches(query, normalized.keys(), n=1, cutoff=0.7)
        if matches:
            return self.flat[normalized[matches[0]]]

        # final fallback substring match
        for nk, orig in normalized.items():
            if query in nk:
                return self.flat[orig]

        return None
