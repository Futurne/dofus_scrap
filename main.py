#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Scrapping script.
Entry point to all scrapping modules.
"""

import os
import sys
import time
import argparse

from pprint import pprint

from src.scrap.almanax_scrap import ScrapAlmanax
from src.scrap.encyclopedia_scrap import BASENAME_URLS, EncyclopediaScrap
from src.scrap.encyclopedia_item import ScrapItem


def test_on_examples():
    """Scrap some encyclopedia items to test
    if the scrapping is properly done.
    """
    scrap = EncyclopediaScrap()
    scrap.start()

    urls = [
        'https://www.dofus.com/fr/mmorpg/encyclopedie/armes/26011-faux-chaotique',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/equipements/17581-collier-valet-veinard',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/panoplies/344-panoplie-reine-voleurs',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/monstres/2385-abrakadnuzar',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/familiers/11966-blerodoudou',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/montures/37-dragodinde-amande-ivoire',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/consommables/11505-potion-torboyo',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/ressources/13923-moustache-klime',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/objets-d-apparat/23110-bandeau-yonkwa',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/compagnons/22-andre-sage',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/idoles/18-bihilete-mineure',
        'https://www.dofus.com/fr/mmorpg/encyclopedie/harnachements/17838-harnachement-dragodinde-pilote',
    ]
    for url in urls:
        time.sleep(5)
        item = ScrapItem(scrap.driver, url)
        item.scrap_page()
        print(f'[{item.item_name}]:')
        pprint(item.to_dict())
        print('\n', end='')

    scrap.driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download Dofus datasets')

    parser.add_argument(
        '--test',
        action='store_true',
        help='Test the scrapper on a subset of pages and then quit'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Download every datasets'
    )
    parser.add_argument(
        '--almanax',
        action='store_true',
        help='Download from the almanax website'
    )
    for arg_name in sorted(BASENAME_URLS.keys()):
        parser.add_argument(
            f'--{arg_name}',
            action='store_true',
            help=f'Download from the encyclopedia {arg_name} page'
        )

    args = parser.parse_args()
    if args.test:
        test_on_examples()
        sys.exit(os.EX_OK)

    if args.all:
        args.almanax = True
        for category in BASENAME_URLS.keys():
            args.__dict__[category] = True

    # Create the 'data' directory if necessary
    if not os.path.isdir('data_raw'):
        os.makedirs('data_raw')

    if args.almanax:
        almanax = ScrapAlmanax()
        almanax.scrap()
        almanax.to_csv('data/almanax.csv')

    for category, url in BASENAME_URLS.items():
        if args.__dict__[category]:
            scrap = EncyclopediaScrap()
            scrap.start(url)
            scrap.scrap_category(url)
            scrap.driver.quit()

