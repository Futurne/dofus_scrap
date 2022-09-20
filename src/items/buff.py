#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Buff:
    def __init__(
        self,
        nom: str,
        poids: int = None,
    ):
        self.nom = nom
        self.poids = poids

    def __eq__(self, other: 'self') -> bool:
        return self.nom == other.nom and self.poids == other.poids

