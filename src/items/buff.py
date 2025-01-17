#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy
from typing import Optional

from src.preprocess.parse_json import VALID_BUFFS

# Init VALID_BUFFS with some other buffs
VALID_BUFFS = copy(VALID_BUFFS)
VALID_BUFFS |= {"Spécial"}
for element in ["Agilité", "Force", "Chance", "Intelligence", "Vitalité", "Sagesse"]:
    VALID_BUFFS |= {f"{element} de base"}
VALID_BUFFS |= {"Niveau d'alignement"}


class Buff:
    def __init__(
        self,
        nom: str,
        poids: Optional[int] = None,
    ):
        self.nom = nom
        self.poids = poids

        assert nom in VALID_BUFFS

    def __eq__(self, other) -> bool:
        return self.nom == other.nom and self.poids == other.poids
