#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union

ELEMENTS = {
    "Air",
    "Eau",
    "Feu",
    "Neutre",
    "Terre",
}


class Degat:
    def __init__(
        self,
        element: str,
        values: Union[tuple[int, int], list[int]],
        vol: bool,
    ):
        self.element = element
        self.values = tuple(values)
        self.vol = vol

        assert element in ELEMENTS

    def __eq__(self, other) -> bool:
        return self.element == other.element and self.values == other.values

    @staticmethod
    def from_dict(degat: dict):
        vol = degat.pop("vol")
        element = next(iter(degat))
        values = degat[element]
        return Degat(element, values, vol)
