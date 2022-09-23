#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from src.items.buff import Buff
from src.items.effet import Effet
from src.items.conditions import ConditionsFeuille, ConditionsNoeud
from src.items.ressource import Ressource


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


def test_ressource_parsing():
    parsed_json = {
        "nom": "Frostiz",
        "url": "https://www.dofus.com/fr/mmorpg/encyclopedie/ressources/11109-frostiz",
        "illustration_url": "https://static.ankama.com/dofus/www/game/items/200/34552.png",
        "Type": "Céréale",
        "description": "Cette céréale est surprenante, en plus de résister au climat extrême de Frigost, elle donne un goût de chocolat au lailait dans lequel elle est plongée.",
        "niveau": 200,
        'effets': {
          "Spécial": [
            "3",
            "Rage du Mulou (niveau 200) : • Le porteur gagne 5% de dommages finaux pendant 2 tours à chaque mort d'un allié (hors invocations) présent au début du combat (cumulable 2 fois)."
          ]
        },
        "conditions": {
            "null": [
                {
                    "spécial": "Quête 'Rencontres d’un soir' achevée"
                }
            ]
        }
    }

    effets = [
        Effet(Buff('Spécial'), special='3'),
        Effet(Buff('Spécial'), special="Rage du Mulou (niveau 200) : • Le porteur gagne 5% de dommages finaux pendant 2 tours à chaque mort d'un allié (hors invocations) présent au début du combat (cumulable 2 fois).")
    ]
    conditions = ConditionsNoeud.from_dict(parsed_json['conditions'])
    parsed_object = Ressource(
        'https://www.dofus.com/fr/mmorpg/encyclopedie/ressources/11109-frostiz',
        'Frostiz',
        'https://static.ankama.com/dofus/www/game/items/200/34552.png',
        'Ressources',
        'Céréale',
        200,
        'Cette céréale est surprenante, en plus de résister au climat extrême de Frigost, elle donne un goût de chocolat au lailait dans lequel elle est plongée.',
        effets,
        conditions
    )

    assert Ressource.from_dict(parsed_json) == parsed_object
