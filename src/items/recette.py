#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.items.interfaces import DofusData

class Recette(DofusData):
    def __init__(
        self,
        name: str,
        item_url: str,
        metier: str,
        level: str,
        recette: list[tuple[int, str]]
    ):
        self.name = name
        self.item_url = item_url
        self.metier = metier
        self.level = level
        self.recette = recette

    def __str__(self) -> str:
        return f'[Recette {self.name}]'

    def to_dict(self) -> str:
        return {
            'url': self.item_url,
            'nom': self.name,
            'metier': self.metier,
            'niveau': self.level,
            'recette': self.recette,
        }

