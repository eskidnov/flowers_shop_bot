# -*- coding: utf-8 -*-
import sqlite3
import random

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self, table="shop"):
        """ Получаем все строки из таблицы table """
        with self.connection:
            # TODO: SQL injection???
            return self.cursor.execute('SELECT * FROM ' + table).fetchall()

    def insert_request(self, name, email, phone, address, buys_list, summary_cost, comment, status):
        print (name, email, phone, address, buys_list, summary_cost, comment, status)
        with self.connection:
            return self.cursor.execute('INSERT INTO flowers_request VALUES (DEFAULT,?,?,?,?,?,?,?,?)', \
                (name, email, phone, str(address), buys_list, int(summary_cost), comment, status,))

    def select_single(self, rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM shop WHERE id = ?', (rownum,)).fetchall()[0]

    def select_page(self, rownum, page_size):
        """ Получаем page_size строк, начиная с rownum"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM shop LIMIT ?,?', (rownum, page_size,)).fetchall()

    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM shop').fetchall()
            return len(result)

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
