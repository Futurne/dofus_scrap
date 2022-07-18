#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from selenium import webdriver
from pprint import pprint

from src.scrap.item import ScrapItem
from src.scrap.equipement import ScrapArme, ScrapEquipement
from src.encyclopedia_scrap import EncyclopediaScrap

if __name__ == '__main__':
    scrap = EncyclopediaScrap()
    scrap.start()

    # scrap = EncyclopediaWeapon(scrap.driver, 'https://www.dofus.com/fr/mmorpg/encyclopedie/armes/20353-crocobur')
    # scrap = EncyclopediaWeapon(scrap.driver, 'https://www.dofus.com/fr/mmorpg/encyclopedie/armes/19270-arc-corrompu')
    # scrap = EncyclopediaWeapon(scrap.driver, 'https://www.dofus.com/fr/mmorpg/encyclopedie/equipements/14076-coiffe-comte-harebourg')
    scrap = ScrapEquipement(scrap.driver, 'https://www.dofus.com/fr/mmorpg/encyclopedie/equipements/14162-sangle-ouare')
    scrap.scrap()
    print(scrap)
    pprint(scrap.to_item().to_dict())

    scrap = ScrapArme(scrap.driver, 'https://www.dofus.com/fr/mmorpg/encyclopedie/armes/19096-marteau-katrepat')
    scrap.scrap()
    print('\n\n', scrap)
    pprint(scrap.to_item().to_dict())
    scrap.driver.quit()

    """
    con = sqlite3.connect('example.db')
    cur = con.cursor()

    scrap.save_to_db(cur)

    con.commit()
    con.close()
    """

