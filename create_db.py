#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
from sqlite3 import Connection


def create_bonus_table(con: Connection):
    command = """
        CREATE TABLE bonus (bonus_id INTEGER PRIMARY KEY, type TINYTEXT)
    """
    cur = con.cursor()
    cur.execute(command)


def create_armes_table(con: Connection):
    command = """
        CREATE TABLE armes
        (
            arme_id INTEGER PRIMARY KEY,
            nom TINYTEXT NOT NULL,
            description TEXT NOT NULL,
            cout_pa UNSIGNED TINYINT,
            po_min UNSIGNED TINYINT,
            po_max UNSIGNED TINYINT,
            critical_chance FLOAT,
            critical_bonus UNSIGNED TINYINT
        )
    """
    cur = con.cursor()
    cur.execute(command)


def create_armes_id_bonus_id(con: Connection):
    command = """
        CREATE TABLE armes_bonus
        (
            arme_id INTEGER NOT NULL,
            bonus_id INTEGER NOT NULL,
            PRIMARY KEY(arme_id, bonus_id),
            FOREIGN KEY (arme_id) REFERENCES armes(arme_id),
            FOREIGN KEY (bonus_id) REFERENCES armes(bonus_id)
        )
    """
    cur = con.cursor()
    cur.execute(command)


def create_database(filename: str):
    if os.path.exists(filename):
        os.remove(filename)

    con = sqlite3.connect(filename)

    create_armes_table(con)
    create_bonus_table(con)
    create_armes_id_bonus_id(con)

    con.commit()
    con.close()


if __name__ == "__main__":
    create_database("example.db")
