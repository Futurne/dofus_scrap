#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        description: str = None,
        effets: list[Effet] = None,
        conditions: ConditionsNoeud = None,
        recette: Recette = None,
    ):
        super().__init__(url, False, nom, illu_url, categorie, type_or_race)
        self.niveau = niveau
        self.description = description
        self.effets = effets
        self.condititions = conditions
        self.recette = recette

