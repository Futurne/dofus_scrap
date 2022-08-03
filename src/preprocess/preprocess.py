#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Apply basic transformations to the raw downloaded data.
"""

from typing import Any, Union


def rename_containers(item: dict[str, Any]) -> dict[str, Any]:
    """Some containers are not well named.
    """
    swap_name = {
        s: 'issu du croisement'
        for s in [
            'issu du croisement (1 croisement possible)',
            'issu du croisement (10 croisements possibles)',
            'issu du croisement (3 croisements possibles)',
            'issu du croisement (4 croisements possibles)',
            'issu du croisement (5 croisements possibles)',
            'issu du croisement (7 croisements possibles)',
            'issu du croisement (8 croisements possibles)',
            'issu du croisement (9 croisements possibles)',
        ]
    }

    if 'containers' not in item:
        return item

    renamed = dict()
    for c_name, c_value in item['containers'].items():
        c_name = swap_name[c_name] if c_name in swap_name else c_name
        renamed[c_name] = c_value

    item['containers'] = renamed
    return item


def preprocess_strings(
        item: Union[str, list[Any], dict[str, Any], Any]
) -> Union[str, list[Any], dict[str, Any], Any]:
    """Correct some values.
    """
    match item:
        case str():
            item = item.replace(r'{~ps}{~zs}', '(s)')
        case list():
            item = [preprocess_strings(s) for s in item]
        case dict():
            item = {c: preprocess_strings(v) for c, v in item.items()}
        case _:
            pass

    return item


def preprocess_item(item: dict[str, Any]) -> dict[str, Any]:
    """Apply all the preprocessing steps to the item.
    """
    item = preprocess_strings(item)
    item = rename_containers(item)
    return item


def remove_containers(item: dict[str, Any], to_remove: set[str]):
    """Remove unwanted containers from the item if it has them.
    """
    if 'containers' not in item:
        return None

    for c_name in to_remove:
        if c_name in item['containers']:
            del item['containers'][c_name]

