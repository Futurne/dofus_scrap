#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Union

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


CONTAINER_CLASS = 'ak-container.ak-panel'
TITLE_CLASS = 'ak-panel-title'
CONTENT_CLASS = 'ak-panel-content'
LIST_CLASS = 'ak-content-list'
ITEM_LIST_CLASS = 'ak-list-element'
ITEM_TITLE_CLASS = 'ak-title'
SELECT_CLASS = 'ak-select-container'

VALID_CONTAINER_TITLES = {
    'description',
    'bonus de la panoplie',
    'composition',
    'effets évolutifs',
    'conditions',
    'caractéristiques',
    'résistances',
    'butins',
    'effets',
    'recette',
    'bonus',
    'sorts',
    'de la même famille',
    "comment l'obtenir ?",
    'issu du croisement',
}


class ScrapItem:
    def __init__(self, driver: webdriver.Firefox, url: str):
        self.driver = driver
        self.url = url
        self.data = dict()

    def get_containers(self) -> dict[str, WebElement]:
        containers = dict()

        for element in self.driver.find_elements(By.CLASS_NAME, CONTAINER_CLASS):
            if not ScrapItem.valid_container(element):
                continue

            title = element.find_element(By.CLASS_NAME, TITLE_CLASS).text
            containers[title] = element.find_element(By.CLASS_NAME, CONTENT_CLASS)

        return containers

    def update_all_forms(self):
        total_forms = len(self.driver.find_elements(By.TAG_NAME, 'form'))
        for form_id in range(total_forms):
            form_element = self.driver.find_elements(By.TAG_NAME, 'form')[form_id]
            try:
                select = form_element.find_element(By.TAG_NAME, 'select')
                select = Select(select)
                values = [int(o.get_attribute('value')) for o in select.options]
                select.select_by_value(str(max(values)))
            except NoSuchElementException:
                continue

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
        self.item_type = element.text

    def scrap_level(self):
        element = self.driver.find_element(By.CLASS_NAME, 'ak-encyclo-detail-level')
        self.item_level = element.text
    
    def scrap_page(self):
        self.driver.get(self.url)
        self.update_all_forms()

        self.scrap_name()
        self.scrap_illustration()
        self.scrap_type()
        self.scrap_level()

        # Scrap containers
        containers = self.get_containers()
        for category, element in containers.items():
            self.data[category.lower()] = ScrapItem.scrap_container(element)

    def to_dict(self) -> dict:
        data = {
            'nom': self.item_name,
            'url': self.url,
            'illustration_url': self.illustration_url,
            'type': self.item_type,
            'containers': {
                category: value
                for category, value in self.data.items()
                if value not in [[], '']
            },
        }

        if self.item_level != '':
            data['niveau'] = self.item_level

        if self.item_type != '':
            data['type'] = self.item_type

        return data

    @staticmethod
    def valid_container(element: WebElement) -> bool:
        title_count, content_count = 0, 0
        for child in element.find_elements(By.XPATH, './*'):
            if TITLE_CLASS in child.get_attribute('class'):
                title = child.text.lower()
                title_count += int(any(
                    title.startswith(v) for v in VALID_CONTAINER_TITLES
                ))  # Valid only if it starts with one of the valid container titles

            if CONTENT_CLASS in child.get_attribute('class'):
                content_count += 1

        return title_count == 1 and content_count == 1

    @staticmethod
    def scrap_container(element: WebElement) -> Union[str, list[str], list[list[str]]]:
        def scrap_list(element: WebElement) -> list[str]:
            data = []
            for el in element.find_elements(By.CLASS_NAME, ITEM_LIST_CLASS):
                e = el.find_element(By.CLASS_NAME, ITEM_TITLE_CLASS)
                e = e.text if e.text != '' else e.get_attribute('textContent').strip()

                if len(el.find_elements(By.CLASS_NAME, 'ak-text')) != 0:
                    e += ' | ' + ' | '.join([t.text.strip() for t in el.find_elements(By.CLASS_NAME, 'ak-text')])

                data.append(e)
            return data

        if len(element.find_elements(By.CLASS_NAME, LIST_CLASS)) == 1:
            return scrap_list(element.find_element(By.CLASS_NAME, LIST_CLASS))
        elif len(element.find_elements(By.CLASS_NAME, LIST_CLASS)) != 0:
            return [
                scrap_list(element_list)
                for element_list in element.find_elements(By.CLASS_NAME, LIST_CLASS)
            ]
        else:
            return element.text

