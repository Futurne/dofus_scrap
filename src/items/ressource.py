#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional

from src.items.element import Element
from src.items.conditions import ConditionsNoeud
from src.items.effet import Effet
from src.items.recette import Recette


class Ressource(Element):
    def __init__(
        self,
        url: str,
        nom: str,
        illu_url: str,
        categorie: str,
        type_or_race: str,
        niveau: int,
        description: Optional[str] = None,
        effets: Optional[list[Effet]] = None,
        conditions: Optional[ConditionsNoeud] = None,
        recette: Optional[Recette] = None,
    ):
        super().__init__(url, False, nom, illu_url, categorie, type_or_race)
        self.niveau = niveau
        self.description = description
        self.effets = effets
        self.conditions = conditions
        self.recette = recette

    def __eq__(self, other) -> bool:
        tests = [
            super().__eq__(other),
            self.niveau == other.niveau,
            self.description == other.description,
            self.effets == other.effets,
            self.conditions == other.conditions,
            self.recette == other.recette,
        ]
        return all(tests)

    @staticmethod
    def from_dict(element: dict):
        effets = None
        if 'effets' in element:
            effets = Effet.from_multiple(element['effets'])

        conditions = ConditionsNoeud.from_dict(element['conditions']) if 'conditions' in element else None
        return Ressource(
            element['url'],
            element['nom'],
            element['illustration_url'],
            'Ressources',
            element['Type'],
            element['niveau'],
            element['description'] if 'description' in element else None,
            effets,
            conditions,
            recette = None  # Do not build recette yet, wait for all the items to be in db
        )

    def to_dict(self) -> dict:
        raise RuntimeError('Not implemented error')
