#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        items: list[Element],
        bonus: list[list[Effet]],
    ):
        super().__init__(url, False, nom, illu_url, categorie, type_or_race)
        self.items = items
        self.bonus = bonus

    @staticmethod
    def from_dict(element: dict[str, any]) -> 'self':
        bonus = [
            [
                Effet.from_dict(e) for e in bonus_p
            ]
            for bonus_p in element['bonus de la panoplie']
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

    def to_dict(self) -> dict[str, any]:
        raise RuntimeError('Not implemented')

