#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.items.interfaces import Bonus, Condition, DofusData, Dommage


class Item(DofusData):
    def __init__(
        self,
        url: str,
        name: str,
        desc: str,
        level: int,
        type: str,
        illu_url: str,
    ):
        self.url = url
        self.name = name
        self.desc = desc
        self.level = level
        self.type = type
        self.illu_url = illu_url

    def __str__(self) -> str:
        return f'[{self.name}]'

    def to_dict(self) -> str:
        return {
            'url': self.url,
            'nom': self.name,
            'description': self.desc,
            'niveau': self.level,
            'type': self.type,
            'illustration_url': self.illu_url
        }

