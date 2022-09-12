#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union

import pytest

from src.preprocess.parse_json import JsonParser


@pytest.mark.parametrize(
    'to_parse, key, value',
    [
        ('Type : Type1', 'Type', 'Type1'),
        ('Result : Type2', 'Result', 'Type2'),
    ],
)
def test_type_parsing(to_parse: str, key: str, value: str):
    parser = JsonParser()
    parser.parse_type('type', to_parse)
    assert parser.parsed_data == {key: value}


@pytest.mark.parametrize(
    'to_parse, result',
    [
        (
            'Niveau : 10',
            {'niveau': 10},
        ),
        (
            'Niveau : 7 à 11',
            {'niveau': (7, 11)},
        )
    ]
)
def test_niveau_parsing(to_parse: str, result: dict):
    parser = JsonParser()
    parser.parse_niveau('niveau', to_parse)
    assert parser.parsed_data == result


@pytest.mark.parametrize(
    'to_parse, result',
    [
        (
            ['Terre : De 5% à 19%', 'Air : De -6% à 1%'],
            {'résistances': [
                {'Terre': (5, 19)},
                {'Air': (-6, 1)},
            ]}
        ),
    ]
)
def test_resistances_parsing(to_parse: list[str], result: dict):
    parser = JsonParser()
    parser.parse_resistances('résistances', to_parse)
    assert parser.parsed_data == result


@pytest.mark.parametrize(
    'to_parse, result',
    [
        (
            ["Bonus d'expérience 50", 'Bonus de butin 10'],
            {'bonus': {
                "Bonus d'expérience": 50,
                'Bonus de butin': 10,
            }}
        ),
    ]
)
def test_bonus_parsing(to_parse: list[str], result: dict):
    parser = JsonParser()
    parser.parse_bonus('bonus', to_parse)
    assert parser.parsed_data == result


@pytest.mark.parametrize(
    'to_parse, result',
    [
        (
            ['Some item | 10.3 %', 'Some other item | 10.5 - 35 %'],
            {'butins': {
                "Some item": 10.3,
                'Some other item': (10.5, 35),
            }}
        ),
        (
            [
                ['Some item | 10.3 %', 'Some other item | 10.5 - 35 %'],
                ['Conditional item | 3.5 %', 'Another one | 50.7 %'],
            ],
            {
                'butins': {
                    "Some item": 10.3,
                    'Some other item': (10.5, 35),
                },
                'butins conditionnés': {
                    'Conditional item': 3.5,
                    'Another one': 50.7,
                }
            }
        ),
    ]
)
def test_butins_parsing(to_parse: list[Union[str, list[str]]], result: dict):
    parser = JsonParser()
    parser.parse_butins('butins', to_parse)
    assert parser.parsed_data == result


@pytest.mark.parametrize(
    'to_parse, result',
    [
        (
            ['Some item | Item category | 2 x', 'Some other item | Item category | 13 x'],
            {'recette': {
                'Some item': 2,
                'Some other item': 13,
            }}
        ),
    ]
)
def test_recette_parsing(to_parse: list[str], result: dict):
    parser = JsonParser()
    parser.parse_recette('recette', to_parse)
    assert parser.parsed_data == result


@pytest.mark.parametrize(
    'to_parse, result',
    [
        (
            'Muldo dorée\nMuldo capricorne',
            {'issu du croisement': [
                ('Muldo dorée', 'Muldo capricorne'),
            ]}
        ),
        (
            'Muldo dorée\nMuldo capricorne\nDragodinde armure\nDragodinde autre',
            {'issu du croisement': [
                ('Muldo dorée', 'Muldo capricorne'),
                ('Dragodinde armure', 'Dragodinde autre'),
            ]}
        ),
    ]
)
def test_croisements_parsing(to_parse: str, result: dict):
    parser = JsonParser()
    parser.parse_croisements('issu du croisement', to_parse)
    assert parser.parsed_data == result


@pytest.mark.parametrize(
    'to_parse, result',
    [
        (
            'Amulette du Piou\nAmulette\nNiv 11',
            {'composition': [
                'Amulette du Piou',
            ]}
        ),
        (
            'Amulette du Piou\nAmulette\nNiv 11 Voir la recette\nAnneau du Piou Rouge\nAnneau\nNiv 12',
            {'composition': [
                'Amulette du Piou',
                'Anneau du Piou Rouge',
            ]}
        ),
    ]
)
def test_croisements_parsing(to_parse: str, result: dict):
    parser = JsonParser()
    parser.parse_composition_pano('composition', to_parse)
    assert parser.parsed_data == result


@pytest.mark.parametrize(
    'to_parse, result',
    [
        (
            ['Génération : 1', 'Nombre de pods : 600', "Taux d'apprentissage : 20%", 'Capturable : Non', 'Test : Oui'],
            {'caractéristiques': {
                'Génération': 1,
                'Nombre de pods': 600,
                "Taux d'apprentissage": 20,
                'Capturable': False,
                'Test': True,
            }}
        ),  # Montures
        (
            ['PV : De 4700 à 8000', 'PA : 1', 'PM : -3'],
            {'caractéristiques': {
                'PV': (4700, 8000),
                'PA': 1,
                'PM': -3,
            }}
        ),  # Monstres
        (
            ['PA : 4 (1 utilisation par tour)', 'Portée : 1', 'CC : 1/30 (+15)'],
            {'caractéristiques': {
                'PA': 4,
                'utilisations': 1,
                'Portée': 1,
                'CC': (1, 30),
                'CC bonus': 15,
            }}
        ),  # Armes
        (
            ['PA : 4 (2 utilisations par tour)', 'Portée : 2 à 4', 'CC : 1/0'],
            {'caractéristiques': {
                'PA': 4,
                'utilisations': 2,
                'Portée': (2, 4),
                'CC': (1, 0),
            }}
        ),  # Armes
    ]
)
def test_caracteristiques_parsing(to_parse: str, result: dict):
    parser = JsonParser()
    parser.parse_caracteristiques('caractéristiques', to_parse)
    assert parser.parsed_data == result


@pytest.mark.parametrize(
    'to_parse, result',
    [
        (
            ['Attitude Aura du Touitcheur'],
            {'bonus de la panoplie': [
                [{'special': 'Attitude Aura du Touitcheur'},],
            ]}
        ),
        (
            [['2 Vitalité', '2 Initiative'], ['3 Vitalité', '3 Initiative', '3 Agilité']],
            {'bonus de la panoplie': [
                [{'Vitalité': 2}, {'Initiative': 2}],
                [{'Vitalité': 3}, {'Initiative': 3}, {'Agilité': 3}],
            ]}
        ),
    ]
)
def test_bonus_pano_parsing(to_parse: list[Union[str, list[str]]], result: dict):
    parser = JsonParser()
    parser.parse_bonus_pano('bonus de la panoplie', to_parse)
    assert parser.parsed_data == result


@pytest.mark.parametrize(
    'effets, result',
    [
        (
            [],
            {'effets': {}}
        ),  # Empty effect
        (
            ['4 à 6 Force'],
            {'effets': {
                'Force': (4, 6),
            }}
        ),  # Basic effet
        (
            ['-6 à -4 Force', '-1 PA'],
            {'effets': {
                'Force': (-6, -4),
                'PA': -1
            }}
        ),  # Basic multiple effects and negative values
        (
            ['4 à 6 Force', 'This is a special effect', 'This is another'],
            {'effets': {
                'Force': (4, 6),
                'special': [
                    'This is a special effect',
                    'This is another',
                ]
            }}
        ),  # Special effect
        (
            [
                '1 Dommage(s)',
                '2 à 4% Critique',
                '6 à 10 (dommages Neutre)',
                '10 (vol Feu)',
                '3 à 6 Dommage(s) Terre',
                '3 à 6 Dommage(s) Feu',
                '1 Puissance (pièges)',
                '3 Dommage(s) Pièges',
                '25 à 30 Puissance',
            ],
            {
                'effets': {
                    'Dommage(s)': 1,
                    '% Critique': (2, 4),
                    'Dommage(s) Terre': (3, 6),
                    'Dommage(s) Feu': (3, 6),
                    'Puissance (pièges)': 1,
                    'Dommage(s) Pièges': 3,
                    'Puissance': (25, 30),
                },
                'dégâts': [
                    {'Neutre': (6, 10), 'vol': False},
                    {'Feu': 10, 'vol': True},
                ]
            }
        ),  # Dommage testing
    ]
)
def test_effets_parsing(effets: list[str], result: dict):
    parser = JsonParser()
    parser.parse_effets('effets', effets)
    assert parser.parsed_data == result


@pytest.mark.parametrize(
    'to_parse, result',
    [
        ('Agilité > 30', {'conditions':
            {
                None :[
                    {'>': ('Agilité', 30)},
                ]
            }
        }),  # Basic condition
        ('Sous-zone != Brakmar', {'conditions':
            {
                None :[
                    {'special': 'Sous-zone != Brakmar'},
                ]
            }
        }),  # Shouldn't pick up the 'ou' and should be special
        ('agilité > 30 et intelligence < 40',
            {'conditions':
                {
                    'et' :[
                        {'>': ('agilité', 30)},
                        {'<': ('intelligence', 40)},
                    ]
                }
            }
        ),  # Basic multiple conditions
        ('() et agilité > 30 et intelligence < 40',
            {'conditions':
                {
                    'et' :[
                        {'>': ('agilité', 30)},
                        {'<': ('intelligence', 40)},
                    ]
                }
            }
        ),  # Empty parenthesis should be ignored
        ('agilité > 30 et (intelligence < 40 ou être niveau 200)',
            {'conditions':
                {
                    'et' :[
                        {'>': ('agilité', 30)},
                        {
                            'ou': [
                                {'<': ('intelligence', 40)},
                                {'special': 'être niveau 200'},
                            ],
                        }
                    ]
                }
            }
        ),  # Testing with sub-conditions
        ('()', dict()),
    ]
)
def test_conditions_parsing(to_parse: str, result: dict):
    parser = JsonParser()
    parser.parse_conditions('conditions', [to_parse])
    assert parser.parsed_data == result

