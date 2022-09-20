#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.items.element import Element


class Recette:
    def __init__(
        self,
        items: list[Element],
        quantities: list[int],
    ):
        self.items = items
        self.quantities = quantities

    def __eq__(self, other: 'self') -> bool:
        return self.items == other.items and self.quantities == other.quantities

