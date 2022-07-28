#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from pprint import pprint

from src.parse_json import JsonParser



if __name__ == '__main__':
    filename = 'data/armes.json'
    with open(filename, 'r') as json_file:
        data = json.load(json_file)


    parser = JsonParser(data[1])
    data = parser.parse()
    print(data)

