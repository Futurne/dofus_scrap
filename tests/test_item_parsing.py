#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from src.items.buff import Buff
from src.items.effet import Effet
from src.items.conditions import ConditionsFeuille, ConditionsNoeud


def test_conditions_parsing():
    parsed_json = {
        "et": [
            {
                ">": [
                    "Force",
                    350,
                ]
            },
            {
                ">": [
                    "Agilité de base",
                    350,
                ]
            }
        ]
    }

    feuilles = [
        ConditionsFeuille(
            '>',
            Buff('Force'),
            350,
            None,
        ),
        ConditionsFeuille(
            '>',
            Buff('Agilité de base'),
            350,
            None,
        ),
    ]
    parsed_object = ConditionsNoeud('et', feuilles)
    assert ConditionsNoeud.from_dict(parsed_json) == parsed_object

    parsed_json = {"et": [
        {
            ">": [
                "Force",
                350
            ]
        },
        {
            "ou": [
                {
                    ">": [
                        "Intelligence de base",
                        350
                    ]
                },
                {
                    ">": [
                        "Chance de base",
                        350
                    ]
                },
                {
                    ">": [
                        "Agilité de base",
                        350
                        ]
                }
            ]
        }
    ]}
    feuilles = [
        ConditionsFeuille('>', Buff('Intelligence de base'), 350),
        ConditionsFeuille('>', Buff('Chance de base'), 350),
        ConditionsFeuille('>', Buff('Agilité de base'), 350),
    ]
    children = [
        ConditionsFeuille('>', Buff('Force'), 350),
        ConditionsNoeud('ou', feuilles)
    ]
    parsed_object = ConditionsNoeud('et', children)
    assert ConditionsNoeud.from_dict(parsed_json) == parsed_object

    parsed_json = {
        'null': [{'spécial': 'Objet non équipable'},]
    }
    parsed_object = ConditionsNoeud('null', [ConditionsFeuille('spécial', special_value='Objet non équipable')])
    assert ConditionsNoeud.from_dict(parsed_json) == parsed_object


def test_effet_parsing():
    parsed_json = {
        'Vitalité': [201, 250]
    }
    parsed_object = Effet(Buff('Vitalité'), (201, 250))
    assert Effet.from_dict(parsed_json) == parsed_object

    parsed_json = {
        'Portée': 1,
    }
    parsed_object = Effet(Buff('Portée'), (1, 1))
    assert Effet.from_dict(parsed_json) == parsed_object

    parsed_json = {
        'Spécial': "Le porteur vole de la vie dans son meilleur élément d'attaque en fin de tour aux entités à son contact."
    }
    parsed_object = Effet(Buff('Spécial'), special="Le porteur vole de la vie dans son meilleur élément d'attaque en fin de tour aux entités à son contact.")
    assert Effet.from_dict(parsed_json) == parsed_object

