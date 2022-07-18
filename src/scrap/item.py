#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Collect data from one item page using a selenium session.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By


from src.scrap.interfaces import ItemCasting
from src.items.item import Item


class ScrapItem(ItemCasting):
    """Collect all data from an item page.
    """
    def __init__(self, driver: webdriver.Firefox, item_url: str):
        self.driver = driver
        self.item_url = item_url

        self.item_name = None
        self.illustration_url = None
        self.item_description = None
        self.item_level = None
        self.item_type = None

    def scrap_name(self):
        element = self.driver.find_element(By.CLASS_NAME, 'ak-title-container')
        element = element.find_element(By.TAG_NAME, 'h1')
        raw_html = element.get_attribute('innerHTML')
        name = raw_html.split('\n')[-2]
        self.item_name = name.strip()

    def scrap_illustration(self):
        element = self.driver.find_element(By.CLASS_NAME, 'ak-encyclo-detail-illu')
        element = element.find_element(By.TAG_NAME, 'img')
        self.illustration_url = element.get_attribute('src')

    def scrap_type(self):
        element = self.driver.find_element(By.CLASS_NAME, 'ak-encyclo-detail-type')
        element = element.find_element(By.TAG_NAME, 'span')
        self.item_type = element.text

    def scrap_level(self):
        element = self.driver.find_element(By.CLASS_NAME, 'ak-encyclo-detail-level')
        self.item_level = int(element.text.split(' : ')[-1])

    def scrap_description(self):
        element = self.driver.find_element(By.CLASS_NAME, 'ak-panel-content')
        element = element.find_element(By.CLASS_NAME, 'ak-panel-content')
        self.item_description = element.text

    def scrap(self):
        """Scrap the item page and collect all data.
        """
        self.driver.get(self.item_url)

        self.scrap_name()
        self.scrap_illustration()
        self.scrap_type()
        self.scrap_level()
        self.scrap_description()

    def to_item(self) -> Item:
        return Item(
            self.item_url,
            self.item_name,
            self.item_description,
            self.item_level,
            self.item_type,
            self.illustration_url
        )

    def __str__(self) -> str:
        return f'[{self.item_name}]'

