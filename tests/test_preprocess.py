#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from src.preprocess.preprocess import rename_containers
from src.preprocess.preprocess import preprocess_strings
from src.preprocess.preprocess import remove_containers


@pytest.mark.parametrize(
   'input_name, output_name',
    [
        ('issu du croisement (1 croisement possible)', 'issu du croisement'),
        ('issu du croisement (10 croisements possibles)', 'issu du croisement'),
        ('issus du croisement', 'issus du croisement'),
        ('issu du croisements', 'issu du croisements'),
    ]
)
def test_rename_containers(input_name: str, output_name: str):
    input_item = {
        'containers': {
            input_name: 42,
            'test other container': 10,
        },
        'not a container': 69,
    }
    output_item = {
        'containers': {
            output_name: 42,
            'test other container': 10,
        },
        'not a container': 69,
    }
    assert rename_containers(input_item) == output_item


def test_preprocess_strings():
    item_input = {
        'Test(s)': ['Oui{~ps}{~zs}', 'Non(s)'],
        'Autre chose{~ps}{~zs}': {
            'Autre chose': 'Test {~ps}{~zs}',
        }
    }

    item_output = {
        'Test(s)': ['Oui(s)', 'Non(s)'],
        'Autre chose{~ps}{~zs}': {
            'Autre chose': 'Test (s)',
        }
    }
    
    assert preprocess_strings(item_input) == item_output


def test_remove_containers():
    item_input = {
        'containers': {
            'unwanted': 'Non',
            'effets': 'Oui',
            'unwanted aswell': 'Oh',
            'Yep': 'Ahh',
        },
        'unwanted': 'Keep this one',
        'Hey': 'Hello',
    }
    item_output = {
        'containers': {
            'effets': 'Oui',
        },
        'unwanted': 'Keep this one',
        'Hey': 'Hello',
    }

    remove_containers(item_input, {'unwanted', 'unwanted aswell', 'Yep'})
    assert item_output == item_input

