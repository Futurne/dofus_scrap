#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional

from src.items.element import Element
from src.items.effet import Effet


class Panoplie(Element):
    def __init__(
        self,
        url: str,
        nom: str,
        illu_url: str,
        categorie: str,
        type_or_race: str,
        items: Optional[list[Element]],
        bonus: list[list[Effet]],
    ):
        super().__init__(url, False, nom, illu_url, categorie, type_or_race)
        self.items = items
        self.bonus = bonus

    @staticmethod
    def from_dict(element: dict):
        bonus = []
        for bonus_p in element['bonus de la panoplie']:
            current_dict = dict()
            for effet in bonus_p:
                key, value = next(iter(effet.items()))
                match key:
                    case 'Spécial':
                        if 'Spécial' not in current_dict:
                            current_dict['Spécial'] = []
                        current_dict['Spécial'].append(value)
                    case _:
                        current_dict[key] = value

            bonus.append(current_dict)

        bonus = [
            Effet.from_multiple(bonus_p)
            for bonus_p in bonus
        ]
        return Panoplie(
            element['url'],
            element['nom'],
            element['illustration_url'],
            'Panoplies',
            element['Type'],
            items = None,  # Wait for 'db' to be completed
            bonus = bonus,
        )

    def to_dict(self) -> dict:
        raise RuntimeError('Not implemented')

    def __eq__(self, other) -> bool:
        tests = [
            super().__eq__(other),
            self.items == other.items,
            self.bonus == other.bonus,
        ]
        return all(tests)
