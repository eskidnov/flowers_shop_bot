# -*- coding: utf-8 -*-
import shelve
# from SQL.SQLighter import SQLighter
from config import shelve_name

# def count_rows():
#     """
#     Данный метод считает общее количество строк в базе данных и сохраняет в хранилище.
#     """
#     db = SQLighter(database_name)
#     rowsnum = db.count_rows()
#     with shelve.open(shelve_name) as storage:
#         storage['rows_count'] = rowsnum


def get_rows_count():
    """
    Получает из хранилища количество строк в БД
    :return: (int) Число строк
    """
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['rows_count']
    return rowsnum


def set_basket(user_id):
    """
    Записываем юзера в хранилище.
    :param user_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        storage[str(user_id)] = {}


def get_basket(user_id):
    """
    Получем список товаров в корзине пользователя.
    :param user_id: id пользовател
    :return: (list) Товары в корзине
    """
    with shelve.open(shelve_name) as storage:
        return storage.get(str(user_id), {})


def add_to_basket(user_id, product):
    """
    Добавляем выбранный товар в корзину юзера.
    :param user_id: id юзера
    :param product: товар, добавляемый в хранилище (из БД)
    """
    with shelve.open(shelve_name) as storage:
        temp = storage[str(user_id)]
        if temp.get(product, None):
            temp[product] = temp[product] + 1
        else:
            temp.update({
                product : 1,
            })
        storage[str(user_id)] = temp


def del_from_basket(user_id, product):
    """
    Удаляем выбранный товар из корзины юзера.
    :param user_id: id юзера
    :param product: товар, удаляемый из хранилища (из БД)
    """
    with shelve.open(shelve_name) as storage:
        temp = storage[str(user_id)]
        print(temp)
        try:
            temp.pop(product)
        except:
            print('В корзине нет товара', product.item)
        storage[str(user_id)] = temp


def remove_amount(user_id, product):
    """
    Уменьшает на 1 количество товара в корзине.
    :param user_id: id юзера
    :param product: товар, количество которого уменьшается (из БД)
    """
    with shelve.open(shelve_name) as storage:
        temp = storage[str(user_id)]
        if temp.get(product, None):
            temp[product] = temp[product] - 1
        else:
            print('Такого товара в корзине нет!')
        storage[str(user_id)] = temp


def item_amount(user_id, product):
    """
    Возвращает количество выбранного товара.
    :param user_id: id пользователя
    :param product: товар в корзине (из БД)
    :return: (int) количество товара
    """
    with shelve.open(shelve_name) as storage:
        return storage[str(user_id)].get(product, 0)


def del_user_basket(user_id):
    """
    Очищаем корзину текущего пользователя.
    :param user_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        try:
            del storage[str(user_id)]
        except:
            print('Корзины пользователя не существует!')


def get_answer_for_user(chat_id):
    """
    Получаем правильный ответ для текущего юзера.
    В случае, если человек просто ввёл какие-то символы, не начав игру, возвращаем None
    :param chat_id: id юзера
    :return: (str) Правильный ответ / None
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        # Если человек не играет, ничего не возвращаем
        except KeyError:
            return None