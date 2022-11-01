#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.items.effet import Effet


def bonus_pano_from_list(bonus_list: list) -> list[list[Effet]]:
    bonus = []
    for bonus_p in bonus_list:
        current_dict = dict()
        for effet in bonus_p:
            key, value = next(iter(effet.items()))
            match key:
                case "Spécial":
                    if "Spécial" not in current_dict:
                        current_dict["Spécial"] = []
                    current_dict["Spécial"].append(value)
                case _:
                    current_dict[key] = value

        bonus.append(current_dict)

    bonus = [Effet.from_multiple(bonus_p) for bonus_p in bonus]
    return bonus
