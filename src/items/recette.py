#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Recette:
    def __init__(
        self,
        items: list,
        quantities: list[int],
    ):
        self.items = items
        self.quantities = quantities

    def __eq__(self, other) -> bool:
        return self.items == other.items and self.quantities == other.quantities

    @staticmethod
    def from_dict(recette: dict):
        items, quantities = list(), list()
        for i, q in recette.items():
            items.append(i)
            quantities.append(q)
        return Recette(items, quantities)
