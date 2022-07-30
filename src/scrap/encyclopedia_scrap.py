#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Download data from the encyclopedia website: https://www.dofus.com/fr/mmorpg/encyclopedie.
Uses selenium to keep a human-like session.
"""

import os
import time
import json
from collections import defaultdict

import yaml
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from src.scrap.encyclopedia_item import ScrapItem


BASENAME_URLS = {
    'ressources': 'https://www.dofus.com/fr/mmorpg/encyclopedie/ressources',
    'armes': 'https://www.dofus.com/fr/mmorpg/encyclopedie/armes',
    'equipements': 'https://www.dofus.com/fr/mmorpg/encyclopedie/equipements',
    'familiers': 'https://www.dofus.com/fr/mmorpg/encyclopedie/familiers',
    'montures': 'https://www.dofus.com/fr/mmorpg/encyclopedie/montures',
    'consommables': 'https://www.dofus.com/fr/mmorpg/encyclopedie/consommables',
    'apparats': 'https://www.dofus.com/fr/mmorpg/encyclopedie/objets-d-apparat',
    'compagnons': 'https://www.dofus.com/fr/mmorpg/encyclopedie/compagnons',
    'idoles': 'https://www.dofus.com/fr/mmorpg/encyclopedie/idoles',
    'harnachements': 'https://www.dofus.com/fr/mmorpg/encyclopedie/harnachements',
    'bestiaire': 'https://www.dofus.com/fr/mmorpg/encyclopedie/monstres',
    'panoplies': 'https://www.dofus.com/fr/mmorpg/encyclopedie/panoplies',
}  # category_name -> category_url

TIMEOUT = 3  # To slow down our scrapping (else cloudfare is not happy)


class EncyclopediaScrap:
    """To download every items from a specific category.
    The valid categories can be found in the 'BASENAME_URLS' dictionnary.

    Before downloading the items, the session needs to be initialized by the 'start' method.
    """
    def __init__(self):
        self.driver = webdriver.Firefox()

    def check_for_cookies_panel(self) -> bool:
        """Accept the cookies if the panel is in the page.
        Return wether the cookies have been accepted or not.
        """
        time.sleep(TIMEOUT)  # Wait for the page to fully load

        try:
            element = self.driver.find_element(By.CLASS_NAME, 'ak-block-cookies-infobox')
            buttons = element.find_elements(By.TAG_NAME, 'button')
            for b in buttons:
                if 'ACCEPTER' in b.text:
                    b.click()  # Accept cookies
                    return True
        except NoSuchElementException:
            return False

        raise RuntimeError('Cookies panel has been found but no there is no accept button.')

    def start(self, url: str='https://www.dofus.com/fr'):
        """Load a page and check for cookies.
        The page in itself is not important, as long as it is a Dofus.com page.
        """
        self.driver.get(url)
        self.check_for_cookies_panel()

    def list_items(self, url: str) -> list[str]:
        """Get all items links in the page.
        """
        self.driver.get(url)
        element = self.driver.find_element(By.TAG_NAME, 'tbody')
        trs = element.find_elements(By.TAG_NAME, 'tr')
        items = [
            tr.find_element(By.TAG_NAME, 'a').get_attribute('href')
            for tr in trs
        ]
        return items

    def total_pages(self, url: str) -> int:
        """Detect the number of pages for the specified category pointed the url.
        """
        self.driver.get(url)
        element = self.driver.find_element(By.CLASS_NAME, 'ak-panel-footer')
        lis = element.find_elements(By.TAG_NAME, 'li')
        pages = [
            int(l.text)
            for l in lis
            if l.text.isdecimal()
        ]
        return max(pages)

    def category_name(self, category_url: str) -> str:
        """Return the proper name of the category.
        """
        self.driver.get(category_url)
        element = self.driver.find_element(By.CLASS_NAME, 'ak-title-container')
        element = element.find_element(By.TAG_NAME, 'h1')
        raw_html = element.get_attribute('innerHTML')
        name = raw_html.split('\n')[-2]
        return name.strip()

    def check_404(self, url: str) -> bool:
        """Is the page a 404 error page?
        """
        self.driver.get(url)
        try:
            self.driver.find_element(By.CLASS_NAME, 'ak-404')
            return True
        except NoSuchElementException:
            return False

    def scrap_category(self, category_url: str):
        """Get all items in the category.
        This is a *long* process. There is timeout between each item to
        avoid the 'are you a human?' question.
        Take the 

        Save them into a csv file in the 'data' directory.
        """
        max_page_number = self.total_pages(category_url)
        category_name = self.category_name(category_url).lower()
        filepath = f'data/{category_name}.json'

        # Load the existing df if possible
        if os.path.exists(filepath):
            with open(filepath, 'r') as json_file:
                data = json.load(json_file)
        else:
            data = list()

        # Load the existing encyclopedia state if possible
        state = defaultdict(int)
        if os.path.exists('data/encyclopedia_state.yaml'):
            with open('data/encyclopedia_state.yaml') as state_file:
                state |= yaml.safe_load(state_file)  # Get the dictionnary and make it a defaultdict (thanks to the |= operator)

        for page_number in tqdm(range(state[category_name] + 1, max_page_number + 1)):
            url = EncyclopediaScrap.get_page_number(category_url, page_number)
            items = self.list_items(url)
            for item_url in tqdm(items):
                time.sleep(TIMEOUT)  # Avoid spamming the server

                scrap_item = ScrapItem(self.driver, item_url)
                scrap_item.scrap_page()
                data.append(scrap_item.to_dict())

            # Save the data at the end of the page
            with open(filepath, 'w') as json_file:
                json.dump(data, json_file, ensure_ascii=False)

            # Update the encyclopedia state
            state[category_name] += 1
            with open('data/encyclopedia_state.yaml', 'w') as state_file:
                yaml.dump(dict(state), state_file, allow_unicode=True)

    @staticmethod
    def get_page_number(basename_url: str, number: int) -> str:
        return f'{basename_url}?page={number}'

