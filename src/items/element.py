#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc


CATEGORIES = {
    'Armes',
    'Bestiaire',
    'Compagnons',
    'Consommables',
    'Équippements',
    'Familiers',
    'Harnachements',
    'Idoles',
    'Montures',
    "Objet d'apparats",
    'Panoplies',
    'Ressources',
}


class Element(abc.ABC):
    def __init__(
        self,
        url: str,
        erreur_404: bool,
        nom: str = None,
        illu_url: str = None,
        categorie: str = None,
        type_or_race: str = None,
    ):
        self.url = url
        self.erreur_404 = erreur_404
        self.nom = nom
        self.illu_url = illu_url
        self.categorie = categorie
        self.type_or_race = type_or_race

        if categorie:
            assert categorie in CATEGORIES, f"Category {categorie} not found in the known categories."

    @abc.abstractstaticmethod
    def from_dict(element: dict[str, any]) -> "self":
        pass

    @abc.abstractmethod
    def to_dict(self) -> dict[any]:
        pass

