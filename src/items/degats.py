#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        values: tuple[int, int],
        vol: bool,
    ):
        self.element = element
        self.values = values
        self.vol = vol

        assert element in ELEMENTS

    def __eq__(self, other) -> bool:
        return self.element == other.element and self.values == other.values

    @staticmethod
    def from_dict(degat: dict):
        vol = degat.pop("vol")

        element = next(iter(degat))
        match degat[element]:
            case int() as a:
                values = (a, a)
            case [a, b]:
                values = (a, b)
            case _:
                raise RuntimeError(f"Unknown damages {degat}")

        return Degat(element, values, vol)
