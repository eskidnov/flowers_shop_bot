# -*- coding: utf-8 -*-

from catalog import Catalog
import database_communication

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
    'Доставка',
    'О нас',
    'Контакты',
    'Скидки и бонусы',
]
back_button = 'Назад'

catalog = database_communication.resolve_assortment_tree(database_communication.get_assortment())


"""
Catalog('Наш каталог', [
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
"""

add_to_basket = 'В корзину'
basket = 'Корзина'
confirm_button = 'Оформить заказ'
empty_basket = 'Корзина пуста!'
clear_button = 'Очистить'
pay_button = 'Оплатить'
user_basket = 'Ваш заказ:'
ordering = 'Оформление заказа'
successful_payment = 'Спасибо за покупку! Мы доставим ваш товар на сумму `{} {}` как можно быстрее! Оставайтесь на связи.'


# catalog = [
#     'Букеты',
#     'Розы',
#     'Подарки',
# ]
# bouquets = [
#     'Хризантемы',
#     'Пионы',
# ]
# roses = [
#     'Красные розы',
#     'Белые розы',
# ]
# presents = [
#     'Игрушки из цветов',
#     'Корзины с цветами',
# ]

deputates = 'Депутаты'
menu_return = 'Нажмите кнопку "Назад", чтобы вернуться в основное меню'
now_msg = 'Вы также можете узнать, что происходит именно сейчас'
now = 'Что сейчас происходит?'
FAQ = {
    'Как пройти в Государственную Думу?' : [
        'Георгиевский переулок, д.2, 10-й подъезд',
        55.758721,
        37.614795,
    ],
    'Как пройти в Малый Манеж?' : [
        'Георгиевский переулок, д.3/3',
        55.759630,
        37.615327,
    ]
}
contacts = '_INSTAGRAM_: [@molparlamrf](https://www.instagram.com/molparlamrf/)\n\n_TELEGRAM_: @zotovmedia\n\n'\
           '_VK_: https://vk.com/forumgd2017\n\n_Почта_: mp-rf@mail.ru'
cancel = 'Для отмены и возврата в меню отправьте /start'
cancelled = 'Отменено'
name = 'Ваше имя:'
contact = 'Ваши почта:'
offer = 'Ваше предложение:'
thanks = '_{}_, спасибо за ваш отзыв! В близжайшее время мы рассмотрим ваш вопрос и вышлем ответ по данным контактам:\n_{}_'
error = 'Что-то пошло не так...'

# PHOTOS

botograth_logo = 'AgADAgAD2qgxG8UeWUhPeTYTOwVRmcf7Mg4ABFf7JGovAAFinLeRAAIC'
botograth_caption = 'В случае обнаружения некорректной работы или предложений по совершенствованию Telegram бота, '\
                    'Вы можете обратиться с этим к разработчикам!'
our_contacts = 'Контакты для оперативной связи и предложений:\n\n_Почта_: '\
               'botograth@gmail.com\n\n_Telegram_: @botograth\_adm\n\n_VK_: https://vk.com/botograth'
