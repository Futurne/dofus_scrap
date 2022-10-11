#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional

from src.items.caracteristiques import parse_caracs
from src.items.conditions import ConditionsNoeud
from src.items.degats import Degat
from src.items.effet import Effet
from src.items.panoplie import bonus_pano_from_list
from src.items.recette import Recette

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


class Element:
    def __init__(
        self,
        url: str,
        erreur_404: bool,
        nom: Optional[str] = None,
        illu_url: Optional[str] = None,
        category: Optional[str] = None,
        type_or_race: Optional[str] = None,
        other_properties: Optional[dict[str, any]] = None,
    ):
        self.url = url
        self.erreur_404 = erreur_404
        self.nom = nom
        self.illu_url = illu_url
        self.category = category
        self.type_or_race = type_or_race
        self.other_properties = other_properties

        if category:
            assert (
                category in CATEGORIES
            ), f"Category {category} not found in the known categories."

    def __eq__(self, other) -> bool:
        tests = [
            self.url == other.url,
            self.erreur_404 == other.erreur_404,
            self.nom == other.nom,
            self.illu_url == other.illu_url,
            self.category == other.category,
            self.type_or_race == other.type_or_race,
        ]
        if not all(tests):
            return False

        # Check other properties
        if self.other_properties and other.other_properties:
            if set(self.other_properties.keys()) != set(
                other.other_properties.keys()
            ):  # Check properties name
                return False

            tests = [
                self.other_properties[p] == other.other_properties[p]
                for p in self.other_properties
            ]
            if not all(tests):
                return False

        return True

    @staticmethod
    def from_dict(element: dict):
        pass

    def to_dict(self) -> dict:
        return dict()


def to_item(category: str, data: dict) -> Element:
    element_properties = {"category": category}
    other_properties = dict()

    property_parser = {
        # Basic element properties
        "nom": lambda value: element_properties.update({"nom": value}),
        "url": lambda value: element_properties.update({"url": value}),
        "illustration_url": lambda value: element_properties.update(
            {"illu_url": value}
        ),
        "Type": lambda value: element_properties.update({"type_or_race": value}),
        "Race": lambda value: element_properties.update({"type_or_race": value}),
        "erreur_404": lambda value: element_properties.update({"erreur_404": value}),
        # Other properties
        "conditions": ConditionsNoeud.from_dict,
        "dégâts": lambda value: [Degat.from_dict(v) for v in value],
        "effets": Effet.from_multiple,
        "recette": Recette.from_dict,
        "bonus de la panoplie": bonus_pano_from_list,
        "caractéristiques": lambda value: parse_caracs(category, value),
        "description": lambda value: value,
        "niveau": lambda value: value,
        "composition": lambda value: value,
        "sorts": lambda value: value,
    }
    for property, value in data.items():
        if property not in property_parser:
            raise RuntimeError(f"Cannot parse unknown property {property}")

        parsed_property = property_parser[property](value)
        if parsed_property:
            other_properties[property] = parsed_property

    url = element_properties.pop("url")
    erreur_404 = element_properties.pop("erreur_404", False)
    return Element(
        url,
        bool(erreur_404),
        other_properties=other_properties,
        **element_properties,
    )
