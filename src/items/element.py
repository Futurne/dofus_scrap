#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
from typing import Optional


CATEGORIES = {
    "Armes",
    "Bestiaire",
    "Compagnons",
    "Consommables",
    "Équippements",
    "Familiers",
    "Harnachements",
    "Idoles",
    "Montures",
    "Objet d'apparats",
    "Panoplies",
    "Ressources",
}


class Element(abc.ABC):
    def __init__(
        self,
        url: str,
        erreur_404: bool,
        nom: Optional[str] = None,
        illu_url: Optional[str] = None,
        categorie: Optional[str] = None,
        type_or_race: Optional[str] = None,
    ):
        self.url = url
        self.erreur_404 = erreur_404
        self.nom = nom
        self.illu_url = illu_url
        self.categorie = categorie
        self.type_or_race = type_or_race

        if categorie:
            assert (
                categorie in CATEGORIES
            ), f"Category {categorie} not found in the known categories."

    def __eq__(self, other) -> bool:
        tests = [
            self.url == other.url,
            self.erreur_404 == other.erreur_404,
            self.nom == other.nom,
            self.illu_url == other.illu_url,
            self.categorie == other.categorie,
            self.type_or_race == other.type_or_race,
        ]
        return all(tests)

    @abc.abstractstaticmethod
    def from_dict(element: dict):
        pass

    @abc.abstractmethod
    def to_dict(self) -> dict:
        pass
