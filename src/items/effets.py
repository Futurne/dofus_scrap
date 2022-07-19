#!/usr/bin/env python
# -*- coding: utf-8 -*-
import abc

from src.items.interfaces import Bonus, Condition

class Range(Bonus, Condition):
    def __init__(self, name: str, range: tuple[int]):
        self.name = name
        self.range = range

    def to_dict(self) -> dict:
        return {'élément': self.name, 'range': self.range}


class Special(Bonus, Condition):
    def __init__(self, special: str):
        self.special = special

    def to_dict(self) -> dict:
        return {'spécial': self.special}


class Dommage(Range):
    def __init__(self, name: str, range: tuple[int], steal: bool):
        super().__init__(name, range)
        self.steal = steal

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['vol'] = self.steal
        return data

