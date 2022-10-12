#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Prepare and parse the raw data.
Produces new json files that contains the data in a more structured way.
"""

import argparse
import json
import os

from tqdm import tqdm

from src.preprocess.parse_json import JsonParser
from src.preprocess.preprocess import preprocess_item, remove_containers

to_remove = {
    "armes.json": [],
    "bestiaire.json": ["butins conditionnés"],
    "compagnons.json": ["sorts", "caractéristiques"],
    "consommables.json": [],
    "équipements.json": [],
    "familiers.json": [],
    "harnachements.json": [],
    "idoles.json": [],
    "montures.json": ["comment l'obtenir ?"],
    "objets d'apparat.json": ["effets", "caractéristiques"],
    "panoplies.json": ["bonus total de la panoplie complète"],
    "ressources.json": [],
}  # Filename -> containers to remove


def prepare():
    print("Preprocess data before parsing...")
    for filename in tqdm(to_remove):
        prepared = []
        with open(f"data_raw/{filename}", "r") as json_file:
            data = json.load(json_file)

        for item in data:
            remove_containers(item, to_remove[filename])
            prepared.append(preprocess_item(item))

        with open(f"data/{filename}", "w") as json_file:
            json.dump(prepared, json_file, ensure_ascii=False)


def postprocess(filename: str, data: list[dict]):
    if filename == "bestiaire.json":
        # Monsters can have multiple levels, so we're making sure
        # every "niveau" are tuples.
        for element_id, element in enumerate(data):
            niveau = element["niveau"]
            if type(niveau) is int:
                niveau = (niveau, niveau)
            element["niveau"] = niveau
            data[element_id] = element


def parse_all():
    print("Parse all data...")
    parser = JsonParser()
    for filename in tqdm(os.listdir("./data/")):
        if not filename.endswith(".json"):
            continue

        with open(f"data/{filename}", "r") as json_file:
            data = json.load(json_file)

        parsed_data = [parser.parse(i) for i in data]

        postprocess(filename, parsed_data)

        with open(f"data/{filename}", "w") as json_file:
            json.dump(parsed_data, json_file, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse raw data into a proper JSON file"
    )
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="Prepare parsing by remove some useless containers and doing some preprocessing",
    )
    parser.add_argument(
        "--parse",
        action="store_true",
        help="Parse the prepared raw data, store the new data into a 'data' folder",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Do the `--prepare` and `--parse` in a single tap",
    )

    args = parser.parse_args()
    args.all = args.all or not (
        args.prepare or args.parse
    )  # Do '--all' if no other args are given

    if args.prepare or args.all:
        if not os.path.isdir("data"):
            os.makedirs("data")

        prepare()

    if args.parse or args.all:
        parse_all()
