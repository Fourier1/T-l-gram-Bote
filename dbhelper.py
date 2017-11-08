#! /usr/bin/env python3.5
# -*- coding:utf-8 -*-

"""
CREATION DE LE BASE DE DONNEES
 stock les messages des utilisateurs 
 possibîmlilté de suprimer ces messages 
 possiblilite d'enregistrer ces méssages
 
"""

import sqlite3


class DBHelper:
    """
    Création de la base de données 
    """

    def __init__(self, dbname="todo.sqlite"):
        """
        Création de la BD en lui donnant un nom par defaut et créer la connexion
        :param str dbname: nom de base de donnée
        """
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        """
        Création de Table items de la base de donnée avec un champ descriptioin
        :return: 
        """
        print("Create table")
        tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownerIndex ON items (owner ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.commit()

    def add_item(self, item_text, owner):
        """
        Enregistrer du text dans le champ itms de la table description
        :return: 
        """
        stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, owner):
        """
        Supression d'un item
        :param str item_text: le champ item
        :return: 
        """
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_item(self, owner):
        """
        Renvoie la liste de tous les éléement de notre base de donnée
        :return: 
        """
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner,)
        return [x[0] for x in self.conn.execute(stmt, args)]
