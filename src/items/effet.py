#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import xor
from typing import Optional

from src.items.buff import Buff


class Effet:
    def __init__(
        self,
        buff: Buff,
        values: Optional[tuple[int, int]] = None,
        special: Optional[str] = None,
    ):
        self.buff = buff
        self.values = values
        self.special = special

        assert xor(values is None, special is None)  # One of them has to be None
        assert values is None or values[0] <= values[1]

    def __eq__(self, other) -> bool:
        return (
            self.buff == other.buff
            and self.values == other.values
            and self.special == other.special
        )

    @staticmethod
    def from_dict(effet: dict):
        buff = next(iter(effet))
        if buff == "Spécial":
            return Effet(Buff(buff), special=effet[buff])

        match effet[buff]:
            case int() as a:
                return Effet(Buff(buff), (a, a))
            case [a, b]:
                return Effet(Buff(buff), (a, b))
            case _:
                raise RuntimeError(f"Unknown effect {effet}")

    @staticmethod
    def from_multiple(effets: dict) -> list:
        parsed = []
        for e in effets:
            match e:
                case "Spécial":
                    for value in effets[e]:
                        parsed.append(Effet.from_dict({e: value}))
                case _:
                    parsed.append(Effet.from_dict({e: effets[e]}))
        return parsed
