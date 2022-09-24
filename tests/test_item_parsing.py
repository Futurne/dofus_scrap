#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.items.buff import Buff
from src.items.effet import Effet
from src.items.conditions import ConditionsFeuille, ConditionsNoeud
from src.items.ressource import Ressource
from src.items.panoplie import Panoplie
from src.items.compagnon import Compagnon


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


def test_panoplie_parsing():
    parsed_json = {
        "nom": "Panoplie du Sinistrofu",
        "url": "https://www.dofus.com/fr/mmorpg/encyclopedie/panoplies/275-panoplie-sinistrofu",
        "illustration_url": "https://static.ankama.com/dofus/renderer/look/7b317c38302c323132342c323531357c313d31363736353536342c323d31363335353838332c333d31363737373138352c343d323931303036342c353d31343536313739397c3134307d/full/1/200_200-10.png",
        "Type": "Panoplie",
        "bonus de la panoplie": [
          [
            {
              "Chance": 50
            },
            {
              "Résistance(s) Critiques": 15
            },
            {
              "Résistance(s) Poussée": 30
            }
          ],
          [
            {
              "Chance": 50
            },
            {
              "Résistance(s) Critiques": 15
            },
            {
              "Résistance(s) Poussée": 30
            },
            {
              "PA": 1
            }
          ]
        ],
        "composition": [
          "Cape du Sinistrofu",
          "Amulette du Sinistrofu",
          "Bottes du Sinistrofu"
        ],
        "niveau": 200
    }

    bonus = [
        [
            Effet(Buff('Chance'), (50, 50)),
            Effet(Buff('Résistance(s) Critiques'), (15, 15)),
            Effet(Buff('Résistance(s) Poussée'), (30, 30)),
        ],
        [
            Effet(Buff('Chance'), (50, 50)),
            Effet(Buff('Résistance(s) Critiques'), (15, 15)),
            Effet(Buff('Résistance(s) Poussée'), (30, 30)),
            Effet(Buff('PA'), (1, 1)),
        ]
    ]
    parsed_object = Panoplie(
        'https://www.dofus.com/fr/mmorpg/encyclopedie/panoplies/275-panoplie-sinistrofu',
        'Panoplie du Sinistrofu',
        'https://static.ankama.com/dofus/renderer/look/7b317c38302c323132342c323531357c313d31363736353536342c323d31363335353838332c333d31363737373138352c343d323931303036342c353d31343536313739397c3134307d/full/1/200_200-10.png',
        'Panoplies',
        'Panoplie',
        None,
        bonus,
    )

    assert Panoplie.from_dict(parsed_json) == parsed_object


def test_compagnon_parsing():
    parsed_json = {
        "nom": "Abdoul Heure",
        "url": "https://www.dofus.com/fr/mmorpg/encyclopedie/compagnons/40-abdoul-heure",
        "illustration_url": "https://static.ankama.com/dofus/renderer/look/7b317c3131302c323137352c333939322c343034367c313d236666643237632c323d236539656265302c333d233236333933392c343d233236333933392c353d233133393739317c3134357d/full/1/200_200-10.png",
        "Type": "Compagnon",
        "description": "Encore toute récente, la découverte de la parchomancie fût précurseuse d'une vague d'incarnation sans précédent. Dans l'effervescence générale, de nombreux groupes et guildes se sont formés. L'ordre des Compagnons est de loin le plus mystérieux de ces groupes ; ses membres semblent même déjà maîtriser la parchomancie sur le bout des doigts. Serait-il possible que cette magie ne soit finalement pas si jeune ? En tout cas, une chose est sûre : ces compagnons savent combattre avec style. Abdoul est habillé par le soyeux Barbe Douce, que l'on peut souvent apercevoir en train de coudre dans les reflets des boucliers Hitche."
    }

    parsed_object = Compagnon(
        'https://www.dofus.com/fr/mmorpg/encyclopedie/compagnons/40-abdoul-heure',
        'Abdoul Heure',
        'https://static.ankama.com/dofus/renderer/look/7b317c3131302c323137352c333939322c343034367c313d236666643237632c323d236539656265302c333d233236333933392c343d233236333933392c353d233133393739317c3134357d/full/1/200_200-10.png',
        'Compagnons',
        'Compagnon',
        "Encore toute récente, la découverte de la parchomancie fût précurseuse d'une vague d'incarnation sans précédent. Dans l'effervescence générale, de nombreux groupes et guildes se sont formés. L'ordre des Compagnons est de loin le plus mystérieux de ces groupes ; ses membres semblent même déjà maîtriser la parchomancie sur le bout des doigts. Serait-il possible que cette magie ne soit finalement pas si jeune ? En tout cas, une chose est sûre : ces compagnons savent combattre avec style. Abdoul est habillé par le soyeux Barbe Douce, que l'on peut souvent apercevoir en train de coudre dans les reflets des boucliers Hitche.",
    )

    assert Compagnon.from_dict(parsed_json) == parsed_object
