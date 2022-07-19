#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Scrap all data from a one-year calendar of the Dofus almanax: https://www.krosmoz.com/fr/almanax.
"""

import datetime

import pandas as pd

from src.almanax.almanax_page import AlmanaxPage


class ScrapAlmanax:
    def __init__(self):
        self.base_url = 'https://www.krosmoz.com/fr/almanax/'
        self.data = {
            'date': [],
            'boss_desc': [],
            'rubrikabrax': [],
            'meryde': [],
        }

    def scrap(self):
        day = datetime.date.fromisoformat('2022-01-01')
        delta_day = datetime.timedelta(days=1)
        date_format = '%Y-%m-%d'

        ending_day = day + datetime.timedelta(days=365)  # Care for bisextile years, might be duplicates
        while day < ending_day:
            print(day)
            url = self.base_url + day.strftime(date_format)
            page = AlmanaxPage(url)

            self.data['date'].append(day)
            self.data['boss_desc'].append(page.boss_desc())
            self.data['rubrikabrax'].append(page.rubrikabrax())
            self.data['meryde'].append(page.meryde())

            day += delta_day

    def to_csv(self, filename: str):
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)

    def __str__(self) -> str:
        desc = super().__str__()
        return desc

