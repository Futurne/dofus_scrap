#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.items.buff import Buff
from src.items.conditions import ConditionsFeuille, ConditionsNoeud
from src.items.degats import Degat
from src.items.effet import Effet
from src.items.element import Element, to_item
from src.items.recette import Recette


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
            },
        ]
    }

    feuilles = [
        ConditionsFeuille(
            ">",
            Buff("Force"),
            350,
            None,
        ),
        ConditionsFeuille(
            ">",
            Buff("Agilité de base"),
            350,
            None,
        ),
    ]
    parsed_object = ConditionsNoeud("et", feuilles)
    assert ConditionsNoeud.from_dict(parsed_json) == parsed_object

    parsed_json = {
        "et": [
            {">": ["Force", 350]},
            {
                "ou": [
                    {">": ["Intelligence de base", 350]},
                    {">": ["Chance de base", 350]},
                    {">": ["Agilité de base", 350]},
                ]
            },
        ]
    }
    feuilles = [
        ConditionsFeuille(">", Buff("Intelligence de base"), 350),
        ConditionsFeuille(">", Buff("Chance de base"), 350),
        ConditionsFeuille(">", Buff("Agilité de base"), 350),
    ]
    children = [
        ConditionsFeuille(">", Buff("Force"), 350),
        ConditionsNoeud("ou", feuilles),
    ]
    parsed_object = ConditionsNoeud("et", children)
    assert ConditionsNoeud.from_dict(parsed_json) == parsed_object

    parsed_json = {
        "null": [
            {"spécial": "Objet non équipable"},
        ]
    }
    parsed_object = ConditionsNoeud(
        "null", [ConditionsFeuille("spécial", special_value="Objet non équipable")]
    )
    assert ConditionsNoeud.from_dict(parsed_json) == parsed_object


def test_effet_parsing():
    parsed_json = {"Vitalité": [201, 250]}
    parsed_object = Effet(Buff("Vitalité"), (201, 250))
    assert Effet.from_dict(parsed_json) == parsed_object

    parsed_json = {
        "Portée": (1, 1),
    }
    parsed_object = Effet(Buff("Portée"), (1, 1))
    assert Effet.from_dict(parsed_json) == parsed_object

    parsed_json = {
        "Spécial": "Le porteur vole de la vie dans son meilleur élément d'attaque en fin de tour aux entités à son contact."
    }
    parsed_object = Effet(
        Buff("Spécial"),
        special="Le porteur vole de la vie dans son meilleur élément d'attaque en fin de tour aux entités à son contact.",
    )
    assert Effet.from_dict(parsed_json) == parsed_object


def test_ressource_parsing():
    parsed_json = {
        "nom": "Frostiz",
        "url": "https://www.dofus.com/fr/mmorpg/encyclopedie/ressources/11109-frostiz",
        "illustration_url": "https://static.ankama.com/dofus/www/game/items/200/34552.png",
        "Type": "Céréale",
        "description": "Cette céréale est surprenante, en plus de résister au climat extrême de Frigost, elle donne un goût de chocolat au lailait dans lequel elle est plongée.",
        "niveau": 200,
        "effets": {
            "Spécial": [
                "3",
                "Rage du Mulou (niveau 200) : • Le porteur gagne 5% de dommages finaux pendant 2 tours à chaque mort d'un allié (hors invocations) présent au début du combat (cumulable 2 fois).",
            ]
        },
        "conditions": {"null": [{"spécial": "Quête 'Rencontres d’un soir' achevée"}]},
    }

    effets = [
        Effet(Buff("Spécial"), special="3"),
        Effet(
            Buff("Spécial"),
            special="Rage du Mulou (niveau 200) : • Le porteur gagne 5% de dommages finaux pendant 2 tours à chaque mort d'un allié (hors invocations) présent au début du combat (cumulable 2 fois).",
        ),
    ]
    conditions = ConditionsNoeud.from_dict(parsed_json["conditions"])
    other_properties = {
        "niveau": 200,
        "effets": effets,
        "conditions": conditions,
        "description": "Cette céréale est surprenante, en plus de résister au climat extrême de Frigost, elle donne un goût de chocolat au lailait dans lequel elle est plongée.",
    }
    parsed_object = Element(
        "https://www.dofus.com/fr/mmorpg/encyclopedie/ressources/11109-frostiz",
        False,
        "Frostiz",
        "https://static.ankama.com/dofus/www/game/items/200/34552.png",
        "Ressources",
        "Céréale",
        other_properties,
    )

    assert parsed_object == to_item("Ressources", parsed_json)


def test_panoplie_parsing():
    parsed_json = {
        "nom": "Panoplie du Sinistrofu",
        "url": "https://www.dofus.com/fr/mmorpg/encyclopedie/panoplies/275-panoplie-sinistrofu",
        "illustration_url": "https://static.ankama.com/dofus/renderer/look/7b317c38302c323132342c323531357c313d31363736353536342c323d31363335353838332c333d31363737373138352c343d323931303036342c353d31343536313739397c3134307d/full/1/200_200-10.png",
        "Type": "Panoplie",
        "bonus de la panoplie": [
            [
                {"Chance": (50, 50)},
                {"Résistance(s) Critiques": (15, 15)},
                {"Résistance(s) Poussée": (30, 30)},
            ],
            [
                {"Chance": (50, 50)},
                {"Résistance(s) Critiques": (15, 15)},
                {"Résistance(s) Poussée": (30, 30)},
                {"PA": (1, 1)},
            ],
        ],
        "composition": [
            "Cape du Sinistrofu",
            "Amulette du Sinistrofu",
            "Bottes du Sinistrofu",
        ],
        "niveau": 200,
    }

    bonus = [
        [
            Effet(Buff("Chance"), (50, 50)),
            Effet(Buff("Résistance(s) Critiques"), (15, 15)),
            Effet(Buff("Résistance(s) Poussée"), (30, 30)),
        ],
        [
            Effet(Buff("Chance"), (50, 50)),
            Effet(Buff("Résistance(s) Critiques"), (15, 15)),
            Effet(Buff("Résistance(s) Poussée"), (30, 30)),
            Effet(Buff("PA"), (1, 1)),
        ],
    ]
    other_properties = {
        "bonus de la panoplie": bonus,
        "composition": [
            "Cape du Sinistrofu",
            "Amulette du Sinistrofu",
            "Bottes du Sinistrofu",
        ],
        "niveau": 200,
    }
    parsed_object = Element(
        "https://www.dofus.com/fr/mmorpg/encyclopedie/panoplies/275-panoplie-sinistrofu",
        False,
        "Panoplie du Sinistrofu",
        "https://static.ankama.com/dofus/renderer/look/7b317c38302c323132342c323531357c313d31363736353536342c323d31363335353838332c333d31363737373138352c343d323931303036342c353d31343536313739397c3134307d/full/1/200_200-10.png",
        "Panoplies",
        "Panoplie",
        other_properties,
    )

    assert to_item("Panoplies", parsed_json) == parsed_object


def test_arme_parsing():
    parsed_json = {
        "nom": "Hache Ériphe",
        "url": "https://www.dofus.com/fr/mmorpg/encyclopedie/armes/13896-hache-eriphe",
        "illustration_url": "https://static.ankama.com/dofus/www/game/items/200/19065.png",
        "Type": "Hache",
        "description": "C'est la hache idéale pour faire régner la loi dans les petites localités de l'ouest d'Amakna. Si vous vous en sortez bien, vous aurez un joli badge en forme d'étoile.",
        "effets": {
            "Vitalité": [201, 250],
            "Force": [41, 60],
            "Agilité": [41, 60],
        },
        "dégâts": [
            {"Neutre": [15, 19], "vol": False},
            {"Air": [21, 27], "vol": False},
            {"Terre": [8, 11], "vol": True},
        ],
        "caractéristiques": {
            "PA": 5,
            "utilisations": 1,
            "Portée": [1, 1],
            "CC": [1, 5],
            "CC bonus": 4,
        },
        "conditions": {"et": [{">": ["Force", 350]}, {">": ["Agilité de base", 350]}]},
        "recette": {
            "Galet brasillant": 3,
            "Oreille de Sphincter Cell": 11,
            "Cœur d'Empaillé": 4,
        },
        "niveau": 200,
    }

    effets = [
        Effet(Buff("Vitalité"), [201, 250]),
        Effet(Buff("Force"), [41, 60]),
        Effet(Buff("Agilité"), [41, 60]),
    ]
    degats = [
        Degat("Neutre", [15, 19], False),
        Degat("Air", [21, 27], False),
        Degat("Terre", [8, 11], True),
    ]
    other_properties = {
        "effets": effets,
        "dégâts": degats,
        "recette": Recette(
            ["Galet brasillant", "Oreille de Sphincter Cell", "Cœur d'Empaillé"],
            [3, 11, 4],
        ),
        "caractéristiques": {
            "PA": 5,
            "utilisations": 1,
            "Portée": [1, 1],
            "CC": [1, 5],
            "CC bonus": 4,
        },
        "conditions": ConditionsNoeud.from_dict(parsed_json["conditions"]),
        "niveau": 200,
        "description": "C'est la hache idéale pour faire régner la loi dans les petites localités de l'ouest d'Amakna. Si vous vous en sortez bien, vous aurez un joli badge en forme d'étoile.",
    }
    parsed_object = Element(
        "https://www.dofus.com/fr/mmorpg/encyclopedie/armes/13896-hache-eriphe",
        False,
        "Hache Ériphe",
        "https://static.ankama.com/dofus/www/game/items/200/19065.png",
        "Armes",
        "Hache",
        other_properties,
    )

    assert to_item("Armes", parsed_json) == parsed_object
