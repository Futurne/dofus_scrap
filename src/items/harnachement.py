#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional

from src.items.element import Element
from src.items.conditions import ConditionsNoeud


class Harnachement(Element):
    def __init__(
        self,
        url: str,
        nom: str,
        illu_url: str,
        categorie: str,
        type_or_race: str,
        niveau: int,
        description: Optional[str] = None,
        conditions: Optional[ConditionsNoeud] = None,
    ):
        super().__init__(url, False, nom, illu_url, categorie, type_or_race)
        self.niveau = niveau
        self.description = description
        self.conditions = conditions

    def __eq__(self, other) -> bool:
        tests = [
            super().__eq__(other),
            self.niveau == other.niveau,
            self.description == other.description,
            self.conditions == other.conditions,
        ]
        return all(tests)

    @staticmethod
    def from_dict(element: dict):
        return Harnachement(
            element['url'],
            element['nom'],
            element['illustration_url'],
            'Harnachements',
            element['Type'],
            element['niveau'],
            element['description'] if 'description' in element else None,
            ConditionsNoeud.from_dict(element['conditions']) if 'conditions' in element else None
        )

    def to_dict(self) -> dict:
        raise RuntimeError('Not implemented error')
