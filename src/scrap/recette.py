#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By

from src.scrap.interfaces import ItemCasting
from src.items.recette import Recette

class ScrapRecette(ItemCasting):
    def __init__(
        self,
        driver: webdriver.Firefox,
        item_url: str,
        item_name: str
    ):
        self.driver = driver
        self.item_url = item_url
        self.item_name = item_name
        self.recette = list()
        self.metier = None
        self.level = None

    def scrap_metier(self):
        element = self.driver.find_element(By.CLASS_NAME, 'ak-crafts')
        element = element.find_element(By.CLASS_NAME, 'ak-panel-content')
        element = element.find_element(By.CLASS_NAME, 'ak-panel-intro')
        metier, level = element.text.split(' Niveau ')
        self.metier = metier
        self.level = int(level)

    def scrap_recette(self):
        element = self.driver.find_element(By.CLASS_NAME, 'ak-crafts')
        element = element.find_element(By.CLASS_NAME, 'ak-panel-content')
        element = element.find_element(By.CLASS_NAME, 'ak-content-list')
        for e in element.find_elements(By.CLASS_NAME, 'ak-list-element'):
            item_quantity = e.find_element(By.CLASS_NAME, 'ak-front').text[:-2]
            item_url = e.find_element(By.TAG_NAME, 'a').get_attribute('href')
            self.recette.append((int(item_quantity), item_url))

    def scrap(self):
        self.driver.get(self.item_url)
        self.scrap_metier()
        self.scrap_recette()

    def to_item(self) -> Recette:
        return Recette(
            self.item_name,
            self.item_url,
            self.metier,
            self.level,
            self.recette
        )

