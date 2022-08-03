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
    parser = JsonParser(None)
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
    parser = JsonParser(None)
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
    parser = JsonParser(None)
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
    parser = JsonParser(None)
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
    parser = JsonParser(None)
    parser.parse_butins('butins', to_parse)
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
    parser = JsonParser(None)
    parser.parse_croisements('issu du croisement', to_parse)
    assert parser.parsed_data == result

@pytest.mark.parametrize(
    'effets, result',
    [
        (
            [],
            {'effets': []}
        ),  # Empty effect
        (
            ['4 à 6 Force'],
            {'effets': [
                {'Force': (4, 6)},
            ]}
        ),  # Basic effet
        (
            ['-6 à -4 Force', '-1 PA'],
            {'effets': [
                {'Force': (-6, -4)},
                {'PA': -1}
            ]}
        ),  # Basic multiple effects and negative values
        (
            ['4 à 6 Force', 'This is a special effect'],
            {'effets': [
                {'Force': (4, 6)},
                {'special': 'This is a special effect'}
            ]}
        ),  # Special effect
        (
            ['1 Dommage(s)', '2 à 4% Critique', '6 à 10 (dommages Neutre)', '10 (vol Feu)'],
            {
                'effets': [
                    {'Dommage(s)': 1},
                    {'% Critique': (2, 4)},
                ],
                'dégâts': [
                    {'Neutre': (6, 10), 'vol': False},
                    {'Feu': 10, 'vol': True},
                ]
            }
        ),  # Dommage testing
    ]
)
def test_effets_parsing(effets: list[str], result: dict):
    parser = JsonParser(None)
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
    parser = JsonParser(None)
    parser.parse_conditions('conditions', [to_parse])
    assert parser.parsed_data == result

