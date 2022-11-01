# Dofus Scrapper

This repo contains methods to automatically scrap all data from the [Dofus website](https://www.dofus.com/fr/mmorpg/encyclopedie).
It uses `selenium` to parse the whole encyclopedia, walking from pages to pages and downloading everything.

The end goal is to have a clean database of the items that a player can found in the game.
This database can then be analyzed to find useful insights or can serve as a base for an item recommendation algorithm.

The database can be found on kaggle [here](https://www.kaggle.com/datasets/pstmrtem/dofus-dabase).
It is updated from time to time.

## What it does
1. Scrap all content from [the encyclopedia](https://www.dofus.com/fr/mmorpg/encyclopedie).
2. Scrap all content from [the almanax](https://www.krosmoz.com/fr/almanax).
3. Parse the data into a nice JSON and SQL database.

The corresponding scripts can be launched periodically

## How it works
### Encyclopedia
Content from the encyclopedia is scrapped using `selenium`.
To avoid spamming requests, random pauses are invoked during the scrapping.
In addition to the HTML code of each page, we save the content of some predefined containers.

During the scrapping, some pages can be down, raising a 404 error.
Those pages are still saved so that we can later go back to their URL and try again.

### Almanax
Content from the almanax is scrapped using `requests` and `beautifulsoup`.
This website is lighter than the encyclopedia so we can simply do the requests as fast as possible.
We save the descriptions of each day for a full year (it is a repeating calendar).
Those descriptions can be used to finetune an NLP model.

### Post process
After downloading raw data from the encyclopedia, we need to process this data to have well defined items.
We first parse the raw data into consistent a JSON database, and then we parse those JSON files to get a `PostgreSQL` database.

The SQL database model can be found in the `project_overview.drawio` file (use [drawio](https://www.draw.io/index.html) to read it).


## TODO
* Parse JSON files to produce the SQL database.
* Save HTML pages from the encyclopedia & almanax.
* Retry scrapping from the 404 error items.
* Save more from the almanax website.
* CI/CD : apply black, isort, mypy
* Enhance tests
