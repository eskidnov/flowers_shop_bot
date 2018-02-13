# -*- coding: utf-8 -*-
from SQL.SQLighter import SQLighter
from catalog import Catalog


def get_assortment():
    # download assortment from database 
    # TODO: always open database
    
    database = SQLighter("../../django/db.sqlite3")
    assortment = database.select_all("flowers_productposition")
    database.close()
    return assortment


def check_for_updates(old_assortment):
    # check if assortment changes during work
    assortment = get_assortment()
    if old_assortment == assortment:
        return False
    old_assortment = assortment
    return True


def insert_into_cat(cat, position, data):
    if len(position) == 0:
        cat.categories.append(data)
        return
    for i, subcat in enumerate(cat.categories):
        if subcat.item == position[0]:
            insert_into_cat(subcat, position[1:], data)
            return
    cat.categories.append(Catalog(position[0], []))
    insert_into_cat(cat.categories[-1], position[1:], data)


def resolve_assortment_tree(assortment):
    cat = Catalog('Наш каталог', [])
    for item in assortment:
        # заглушка, пока фоточки неоткуда грузить
        #item[4] = 'https://megaflowers.ru/pub/bouquet/vse-budet-horosho_m.jpg'
        #insert_into_cat(cat, item[5].split(','), Catalog(item[1], [str(item[3]), item[4]]))
        insert_into_cat(cat, item[5].split(','), Catalog(item[1], \
            [str(item[3]), 'https://megaflowers.ru/pub/bouquet/vse-budet-horosho_m.jpg']))
    return cat


def append_request(name, email, phone, address, buys_list, summary_cost, comment):
    # TODO: сделать оправку email
    database = SQLighter("../../django/db.sqlite3")
    database.insert_request(name, email, phone, address, buys_list, summary_cost, comment, 0)