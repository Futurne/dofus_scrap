#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from selenium import webdriver
from pprint import pprint

from src.encyclopedia_scrap import EncyclopediaScrap
from src.encyclopedia_item import ScrapItem


if __name__ == '__main__':
    url = 'https://www.dofus.com/fr/mmorpg/encyclopedie/monstres/384-aboub'
    url = 'https://www.dofus.com/fr/mmorpg/encyclopedie/panoplies/476-panoplie-servitude'
    url = 'https://www.dofus.com/fr/mmorpg/encyclopedie/consommables/11504-pain-frostiz-souffle'
    url = 'https://www.dofus.com/fr/mmorpg/encyclopedie/armes/19096-marteau-katrepat'
    url = 'https://www.dofus.com/fr/mmorpg/encyclopedie/familiers/15978-blokus'
    url = 'https://www.dofus.com/fr/mmorpg/encyclopedie/idoles/20-bihilete-majeure'
    url = 'https://www.dofus.com/fr/mmorpg/encyclopedie/montures/20-dragodinde-amande'
    url = 'https://www.dofus.com/fr/mmorpg/encyclopedie/monstres/47-abraknyde'
    scrap = EncyclopediaScrap()
    scrap.start()

    # scrap = EncyclopediaWeapon(scrap.driver, 'https://www.dofus.com/fr/mmorpg/encyclopedie/armes/20353-crocobur')
    # scrap = EncyclopediaWeapon(scrap.driver, 'https://www.dofus.com/fr/mmorpg/encyclopedie/armes/19270-arc-corrompu')
    # scrap = EncyclopediaWeapon(scrap.driver, 'https://www.dofus.com/fr/mmorpg/encyclopedie/equipements/14076-coiffe-comte-harebourg')
    """
    scrap = ScrapEquipement(scrap.driver, 'https://www.dofus.com/fr/mmorpg/encyclopedie/equipements/14162-sangle-ouare')
    scrap.scrap()
    print(scrap)
    pprint(scrap.to_item().to_dict())
    """

    """
    scrap = ScrapArme(scrap.driver, url)
    scrap.scrap()
    item = scrap.to_item()
    scrap = ScrapRecette(scrap.driver, url, item.name)
    scrap.scrap()
    """
    scrap = ScrapItem(scrap.driver, url)
    scrap.scrap_page()
    data = scrap.to_dict()
    scrap.driver.quit()
    pprint(data)

    """
    con = sqlite3.connect('example.db')
    cur = con.cursor()

    scrap.save_to_db(cur)

    con.commit()
    con.close()
    """

