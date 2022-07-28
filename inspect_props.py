#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from pprint import pprint

from src.parse_json import JsonParser


files = [
    'armes.json',
    'bestiaire.json',
    'compagnons.json',
    'consommables.json',
    'familiers.json',
    'harnachements.json',
    'idoles.json',
    'montures.json',
    "objets d'apparat.json",
    'ressources.json',
    'équipements.json',
]


def all_files():
    for f in files:
        with open(f'data/{f}', 'r') as json_file:
            data = json.load(json_file)
            for item in data:
                yield item


def list_containers_name() -> set[str]:
    names = set()
    for item in all_files():
        if 'containers' in item:
            names |= {c for c in item['containers']}


    return names


def list_all_primary(name: str) -> set:
    primary = set()
    for item in all_files():
        if name in item:
            primary.add(item[name])

    return primary


def list_all_container(name: str) -> set:
    container = set()
    for item in all_files():
        if 'containers' in item and name in item['containers']:
            if type(item['containers'][name]) is list:
                container.add(frozenset(item['containers'][name]))
            else:
                container.add(item['containers'][name])
    return container


def parse_all_effet():
    for item in all_files():
        if 'containers' in item and 'effets' in item['containers']:
            parser = JsonParser(None)
            effets = item['containers']['effets']
            parser.parse_effets('effets', effets)


if __name__ == '__main__':
    names = list_containers_name()
    print('Containers types:')
    pprint(names)

    # p = list_all_primary('type')
    # pprint(p)

    c = list_all_container('conditions')
    pprint(c)

    # parse_all_effet()

