#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional

from src.items.element import Element


class Compagnon(Element):
    def __init__(
        self,
        url: str,
        nom: str,
        illu_url: str,
        categorie: str,
        type_or_race: str,
        description: Optional[str] = None,
    ):
        super().__init__(url, False, nom, illu_url, categorie, type_or_race)
        self.description = description

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.description == other.description

    @staticmethod
    def from_dict(element: dict):
        return Compagnon(
            element['url'],
            element['nom'],
            element['illustration_url'],
            'Compagnons',
            element['Type'],
            element['description'] if 'description' in element else None,
        )

    def to_dict(self) -> dict:
        raise RuntimeError('Not implemented error')
