#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Prepare and parse the raw data.
Produces new json files that contains the data in a more structured way.
"""

import os
import json
import argparse

from src.preprocess.preprocess import preprocess_item, remove_containers
from src.preprocess.parse_json import JsonParser


to_remove = {
    'armes.json': [],
    'bestiaire.json': ['butins conditionnés'],
    'compagnons.json': ['sorts', 'caractéristiques'],
    'consommables.json': [],
    'équipements.json': [],
    'familiers.json': [],
    'harnachements.json': [],
    'idoles.json': [],
    'montures.json': ["comment l'obtenir ?"],
    "objets d'apparat.json": ['effets', 'caractéristiques'],
    'panoplies.json': ['bonus total de la panoplie complète'],
    'ressources.json': [],
}  # Filename -> containers to remove


def prepare():
    for filename in to_remove:
        prepared = []
        with open(f'data_raw/{filename}', 'r') as json_file:
            data = json.load(json_file)

        for item in data:
            remove_containers(item, to_remove[filename])
            prepared.append(preprocess_item(item))

        with open(f'data/{filename}', 'w') as json_file:
            json.dump(prepared, json_file, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse raw data into a proper JSON file')
    parser.add_argument(
        '--prepare',
        action='store_true',
        help='Prepare parsing by remove some useless containers and doing some preprocessing'
    )
    parser.add_argument(
        '--parse',
        action='store_true',
        help='Parse the raw data, store the new data into a \'data\' folder'
    )

    args = parser.parse_args()
    if args.prepare:
        if not os.path.isdir('data'):
            os.makedirs('data')

        prepare()

    if args.parse:
        pass

