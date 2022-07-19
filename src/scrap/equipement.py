#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import Union

from src.scrap.item import ScrapItem
from src.items.effets import Range, Special, Dommage
from src.items.interfaces import Bonus
from src.items.equipement import Equipement, Arme


class ScrapEquipement(ScrapItem):
    def __init__(self, driver: webdriver.Firefox, item_url: str):
        super().__init__(driver, item_url)
        self.item_bonus = []
        self.item_conditions = []

    def scrap_effects(self):
        element = ScrapEquipement.get_panel_attributes(self.driver, 'effets')
        element = element.find_element(By.CLASS_NAME, 'ak-panel-content')
        effects = element.find_elements(By.CLASS_NAME, 'ak-list-element')
        effects = [e.text for e in effects]
        self.item_bonus = [
            ScrapEquipement.bonus_from_string(e)
            for e in effects
        ]

    def scrap_conditions(self):
        element = ScrapEquipement.get_panel_attributes(self.driver, 'conditions')
        if not element:
            return  # No conditions for this item

        conditions = element.find_element(By.CLASS_NAME, 'ak-panel-content')
        conditions = conditions.text
        conditions = conditions.split(' et\n')

        def cond_from_str(cond: str) -> Range:
            assert '<' in cond or '>' in cond
            ineq = '<' if '<' in cond else '>'
            element, value = cond.split(f' {ineq} ')
            if ineq == '<':
                return Range(element, (0, int(value) - 1))
            else:
                return Range(element, (int(value) + 1, 0))

        self.item_conditions = [cond_from_str(c) for c in conditions]

    def scrap(self):
        """Scrap the item page and collect all data.
        """
        super().scrap()
        self.scrap_effects()
        self.scrap_conditions()

    def to_item(self) -> Equipement:
        return Equipement(
            self.item_url,
            self.item_name,
            self.item_description,
            self.item_level,
            self.item_type,
            self.illustration_url,
            self.item_bonus,
            self.item_conditions
        )

    def __str__(self) -> str:
        return f'{super().__str__()} (Equipement)'

    @staticmethod
    def bonus_from_string(string: str) -> Bonus:
        values_regex = r'^-?\d+((\sà\s)?-?\d+)?'
        match_val = re.search(values_regex, string)

        if not match_val:  # Special case, it is a description of an unusual effect
            return Special(string)

        values = match_val.group()
        if 'à' in values:
            min_value, max_value = values.split(' à ')
            min_value, max_value = int(min_value), int(max_value)
        else:
            min_value, max_value = int(values), int(values)

        element = string[match_val.end():].strip()
        return Range(element, (min_value, max_value))

    @staticmethod
    def get_panel_attributes(driver: webdriver.Firefox, title: str):
        main_element = driver.find_element(By.CLASS_NAME, 'ak-encyclo-detail-right')  # Main panel
        element = main_element.find_elements(By.CLASS_NAME, 'ak-container.ak-panel')[1]  # Dive into the second container of the panel
        for e in element.find_elements(By.CLASS_NAME, 'ak-container.ak-panel'):  # Loop through all containers in that container
            panel_title = e.find_element(By.CLASS_NAME, 'ak-panel-title').text
            if panel_title.lower() == title:
                return e


class ScrapArme(ScrapEquipement):
    def __init__(self, driver: webdriver.Firefox, item_url: str):
        super().__init__(driver, item_url)
        self.item_dommages = []
        self.PA = None
        self.n_uses = None
        self.PO = None
        self.critical_chance = None
        self.critical_bonus = None

    def scrap_characteristics(self):
        element = ScrapEquipement.get_panel_attributes(self.driver, 'caractéristiques')
        element = element.find_element(By.CLASS_NAME, 'ak-panel-content')
        effects = element.find_elements(By.CLASS_NAME, 'ak-list-element')
        effects = [e.text for e in effects]
        PA_str, PO_str, CC_str = effects

        # PA
        PA = re.search(r'^PA\s:\s(\d+)', PA_str).group(1)
        self.PA = int(PA)
        n_uses = re.search(r'\((\d+).*\)$', PA_str).group(1)
        self.n_uses = int(n_uses)

        # PO
        PO = re.search(r'\d+(\sà\s\d+)?$', PO_str).group()
        if 'à' in PO:
            min_po, max_po = PO.split(' à ')
            min_po, max_po = int(min_po), int(max_po)
        else:
            min_po, max_po = int(PO), int(PO)
        self.PO = (min_po, max_po)

        # CC
        cc_chance = re.search(r'\d+\/\d+', CC_str).group()
        num, denom = cc_chance.split('/')
        if int(denom) != 0:
            self.critical_chance = int(num) / int(denom)
            cc_bonus = re.search(r'\(\+\d+\)', CC_str).group()
            cc_bonus = cc_bonus[1:-1]  # Remove parenthesis
            self.critical_bonus = int(cc_bonus)
        else:
            self.critical_chance = 0
            self.critical_bonus = 0

    def scrap_effects(self):
        element = self.driver.find_element(By.CLASS_NAME, 'ak-content-list')
        effects = element.find_elements(By.CLASS_NAME, 'ak-list-element')
        effects = [e.text for e in effects]
        effects = [
            ScrapArme.effet_from_string(e)
            for e in effects
        ]

        for effet in effects:
            if isinstance(effet, Dommage):
                self.item_dommages.append(effet)
            else:
                self.item_bonus.append(effet)

    def scrap(self):
        super().scrap()
        self.scrap_characteristics()

    def to_item(self) -> Arme:
        return Arme(
            self.item_url,
            self.item_name,
            self.item_description,
            self.item_level,
            self.item_type,
            self.illustration_url,
            self.item_bonus,
            self.item_conditions,
            self.item_dommages,
            self.PA,
            self.n_uses,
            self.PO,
            self.critical_chance,
            self.critical_bonus
        )

    @staticmethod
    def effet_from_string(string: str) -> Union[Bonus, Dommage]:
        values_regex = r'^-?\d+((\sà\s)?-?\d+)?'
        match_val = re.search(values_regex, string)

        if not match_val:  # Special case, it is a description of an unusual effect
            return Special(string)

        values = match_val.group()
        if 'à' in values:
            min_value, max_value = values.split(' à ')
            min_value, max_value = int(min_value), int(max_value)
        else:
            min_value, max_value = int(values), int(values)

        element = string[match_val.end():].strip()

        damage_regex = r'^\(.*\)$'
        match_damage = re.search(damage_regex, element)
        if not match_damage:
            return Range(element, (min_value, max_value))
        else:
            element = element[1:-1]  # Remove parenthesis
            damage, element = element.split(' ')
            return Dommage(element, (min_value, max_value), damage == 'vol')

