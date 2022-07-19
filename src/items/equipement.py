#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.items.item import Item
from src.items.interfaces import Bonus, Condition
from src.items.effets import Dommage


class Equipement(Item):
    def __init__(
        self,
        url: str,
        name: str,
        desc: str,
        level: int,
        type: str,
        illu_url: str,
        bonus: list[Bonus],
        cond: tuple[list[Condition], str],
    ):
        super().__init__(
            url,
            name,
            desc,
            level,
            type,
            illu_url,
        )

        self.bonus = bonus
        self.cond = cond

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['bonus'] = [b.to_dict() for b in self.bonus]
        data['conditions'] = {
            'valeurs': [c.to_dict() for c in self.cond[0]],
            'bool_op': self.cond[1]
        }
        return data


class Arme(Equipement):
    def __init__(
        self,
        url: str,
        name: str,
        desc: str,
        level: int,
        type: str,
        illu_url: str,
        bonus: list[Bonus],
        cond: list[Condition],
        dommages: list[Dommage],
        PA: int,
        n_uses: int,
        PO: tuple[int],
        critical_chance: float,
        critical_bonus: int,
    ):
        super().__init__(
            url,
            name,
            desc,
            level,
            type,
            illu_url,
            bonus,
            cond
        )

        self.dommages = dommages
        self.PA = PA
        self.n_uses = n_uses
        self.PO = PO
        self.critical_chance = critical_chance
        self.critical_bonus = critical_bonus

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['dommages'] = [d.to_dict() for d in self.dommages]
        data['PA'] = self.PA
        data['n_utilisations'] = self.n_uses
        data['PO'] = self.PO
        data['taux_critique'] = self.critical_chance
        data['bonus_critique'] = self.critical_bonus
        return data

