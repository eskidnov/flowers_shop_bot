# -*- coding: utf-8 -*-

from catalog import Catalog

# TEST
token = '325287100:AAGlQ6zXH0lM28Kx5MPgEReMOyfCeP8REYc'
provider_token = '381764678:TEST:1601'
chanel = -1001145764283

shelve_name = 'shelve.db'

# TEXT
main_menu = 'Основное меню'
main_menu_keyboard = [
    'Наш каталог',
    'Корзина',
    'О нас',
    'Доставка',
    'Скидки и бонусы',
    'Контакты',
]
back_button = 'Назад'

catalog = Catalog('Наш каталог', [
    Catalog('Букеты', [
        Catalog('Хризантемы', [Catalog('Букет 1', ['Цена', 'https://megaflowers.ru/pub/bouquet/vse-budet-horosho_m.jpg']),
                               Catalog('Букет 2', ['Цена', 'https://megaflowers.ru/pub/bouquet/vse-budet-horosho_m.jpg'])]),
        Catalog('Пионы', [Catalog('Букет 3', ['Цена', 'https://megaflowers.ru/pub/bouquet/vse-budet-horosho_m.jpg']),
                          Catalog('Букет 4', ['Цена', 'https://megaflowers.ru/pub/bouquet/vse-budet-horosho_m.jpg'])]),
    ]),
    Catalog('Розы', [
        Catalog('Красные', [Catalog('Букет 5', ['Цена', 'https://megaflowers.ru/pub/bouquet/vse-budet-horosho_m.jpg'])]),
        Catalog('Белые', [Catalog('Букет 6', ['Цена', 'https://megaflowers.ru/pub/bouquet/vse-budet-horosho_m.jpg'])]),
    ]),
    Catalog('Подарки', [
        Catalog('Красные', [Catalog('Букет 7', ['Цена', 'https://megaflowers.ru/pub/bouquet/vse-budet-horosho_m.jpg'])]),
        Catalog('Белые', [Catalog('Букет 8', ['Цена', 'https://megaflowers.ru/pub/bouquet/vse-budet-horosho_m.jpg'])]),
    ]),
])

add_to_basket = 'В корзину'
basket = 'Корзина'
confirm_button = 'Оформить заказ'
empty_basket = 'Корзина пуста!'
clear_button = 'Очистить'
pay_button = 'Оплатить'
user_basket = 'Ваш заказ:'
ordering = 'Оформление заказа'
successful_payment = 'Спасибо за покупку! Мы доставим ваш товар на сумму `{} {}` как можно быстрее! Оставайтесь на связи.'

error_category = 'Такой категории не существует!'

about = [
    'Фото доставки',
    'Отзывы',
    'О компании',
]
company = [
    'Пресса о нас',
    'Наши работы',
]