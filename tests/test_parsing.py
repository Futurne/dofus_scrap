#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.preprocess.parse_json import JsonParser

import pytest


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

