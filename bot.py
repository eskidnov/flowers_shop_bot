# -*- coding: utf-8 -*-

import telebot
import config
import utils
from config import catalog as cat
from database_communication import append_request

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message):
    utils.del_user_basket(message.from_user.id)
    utils.set_basket(message.from_user.id)
    print('Бот запущен пользователем', message.from_user.id)
    bot.send_message(message.chat.id, config.main_menu, parse_mode='markdown', reply_markup=main_menu_keyboard)

@bot.message_handler(commands=['help'])
def help(message):
    print('Пользоватль', message.from_user.id, 'открыл список комманд')
    msg = '/start - запустить бота\n/help - отобразить список доступных команд'
    bot.send_message(message.chat.id, msg, parse_mode='markdown', reply_markup=hidden_keyboard)

@bot.message_handler(func=lambda item: item.text == config.back_button, content_types=['text'])
def back(message):
    """
    Возврат в меню (кнопка "Назад")
    :param message: Сообщение о нажатой кнопке
    """
    print('Пользователь', message.from_user.id, 'вернулся в основное меню')
    bot.send_message(message.chat.id, config.main_menu, reply_markup=main_menu_keyboard)

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[0], content_types=['text'])
def catalog_button(message):
    """
    Обработка нажатия на кнопку "Наш каталог"
    :param message: Сообщение о нажатой кнопке
    """
    # cat - переменная catalog из config.py
    print (cat.get_all_categories())
    print('Пользователь', message.from_user.id, 'открыл "Наш каталог"')
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = (telebot.types.InlineKeyboardButton(text=button_text.item, callback_data=button_text.item)
               for button_text in cat.categories)
    keyboard.add(*buttons)

    bot.send_message(chat_id, '*'+config.main_menu_keyboard[0]+'*', reply_markup=back_keyboard, parse_mode='Markdown')
    bot.send_message(chat_id, '.', reply_markup=keyboard, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda query: query.data in cat.get_all_categories())
def catalog(query):
    category = cat.find(query.data)
    bot.answer_callback_query(query.id)
    print('Пользователь', query.message.from_user.id, 'открыл', category.item)
    if isinstance(category.categories[0].categories[0], str):
        for item in category.categories:
            keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(telebot.types.InlineKeyboardButton(text=config.add_to_basket,
                                                            callback_data=config.add_to_basket+'_'+item.item))
            bot.send_message(query.message.chat.id, '*' + item.item + '*', reply_markup=back_keyboard,
                             parse_mode='Markdown')
            bot.send_photo(query.message.chat.id, caption=item.categories[0], photo=item.categories[1],
                           reply_markup=keyboard)
    else:
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        buttons = (telebot.types.InlineKeyboardButton(text=subcat.item, callback_data=subcat.item)
                   for subcat in category.categories)
        keyboard.add(*buttons)

        bot.delete_message(query.message.chat.id, query.message.message_id - 1)
        bot.delete_message(query.message.chat.id, query.message.message_id)
        bot.send_message(query.message.chat.id, '*'+category.item+'*', reply_markup=back_keyboard, parse_mode='Markdown')
        bot.send_message(query.message.chat.id, 'Выберите нужный вам пункт меню', reply_markup=keyboard)



@bot.callback_query_handler(func=lambda query: config.add_to_basket in query.data)
def add_to_basket(query):
    print(query.data)
    item = query.data.split('_')[1]
    utils.add_to_basket(query.from_user.id, item)
    bot.answer_callback_query(callback_query_id=query.id, text='Успешно добавлено!')



@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[1], content_types=['text'])
def basket(message):
    user_id = message.from_user.id
    user_basket = utils.get_basket(user_id)

    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    confirm_button = telebot.types.KeyboardButton(config.confirm_button)
    clear_button = telebot.types.KeyboardButton(config.clear_button)
    back_button = telebot.types.KeyboardButton(config.back_button)
    keyboard.add(confirm_button, clear_button, back_button)
    bot.send_message(message.chat.id, config.basket, reply_markup=keyboard)
    if user_basket:
        for item in user_basket:
            product = cat.find(item)
            bot.send_message(message.chat.id, '*'+product.item+'*', parse_mode='Markdown')
            bot.send_photo(message.chat.id, caption=product.categories[0], photo=product.categories[1])
    else:
        bot.send_message(chat_id=message.chat.id, text=config.empty_basket)

@bot.message_handler(func=lambda item: item.text == config.clear_button, content_types=['text'])
def clear_basket(message):
    user_id = message.from_user.id
    user_basket = utils.get_basket(user_id)

    for item in user_basket:
        utils.del_from_basket(user_id, item)

    bot.send_message(message.chat.id, config.empty_basket)

@bot.message_handler(func=lambda item: item.text == config.confirm_button, content_types=['text'])
def check_basket(message):
    user_id = message.from_user.id
    user_basket = utils.get_basket(user_id)

    bot.send_message(message.chat.id, config.ordering, reply_markup=back_keyboard)
    if user_basket:
        res = ''
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        pay_button = telebot.types.InlineKeyboardButton(text=config.pay_button, pay=True)
        keyboard.add(pay_button)
        for item in user_basket:
            res += item + '\n'
        # bot.send_message(message.chat.id, res, parse_mode='Markdown', reply_markup=keyboard)

        bot.send_invoice(chat_id=message.chat.id,
                         title=config.user_basket,
                         description=res,
                         invoice_payload='invoice',
                         provider_token=config.provider_token,
                         start_parameter='invoice',
                         currency='rub',
                         prices=[telebot.types.LabeledPrice(label=config.user_basket, amount=10000)],
                         need_name=True,
                         need_phone_number=True,
                         need_shipping_address=True,
                         is_flexible=True,
                         reply_markup=keyboard)
    else:
        bot.send_message(chat_id=message.chat.id, text=config.empty_basket)

def set_shipping_option(id, title, *price):
    shipping_option = telebot.types.ShippingOption(id=id, title=title)
    shipping_option.add_price(*price)
    return shipping_option

@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    bot.answer_shipping_query(shipping_query_id=shipping_query.id,
                              ok=True,
                              shipping_options=[set_shipping_option('delivery', 'Доставка курьером',
                                                                    telebot.types.LabeledPrice('Курьер', 10000)),],
                              error_message='error')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                  ok=True,
                                  error_message='error')


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(chat_id=message.chat.id,
                     text=config.successful_payment.format(message.successful_payment.total_amount / 100,
                                                            message.successful_payment.currency),
                     parse_mode='Markdown')
    order_info = message.successful_payment.order_info
    user_id = message.from_user.id
    user_basket = utils.get_basket(user_id)
    buys_list = ''
    for item in user_basket:
        buys_list += item + '\n'
    append_request(order_info.name, order_info.email, order_info.phone_number, order_info.shipping_address,
                   buys_list, message.successful_payment.total_amount / 100, '')



@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[2], content_types=['text'])
def about(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = (telebot.types.KeyboardButton(text) for text in config.about)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, config.main_menu_keyboard[2], reply_markup=keyboard)



# ВЛАД!!!
# ЗДЕСЬ НАЧИНАЕТСЯ ТВОЙ ПУТЬ
# ТАМ ГДЕ В КАВЫЧКАХ ТЕКСТ - ЗАМЕНЯЙ ЕГО НА ТЕКСТ С КАРТИНОК
# ЧТОБЫ ПЕРЕВЕСТИ СТРОКУ - НАПИШИ \n
# ЧТОБЫ СДЕЛАТЬ ОТСТУП(ТАБУЛЯЦИЮ) - НАПИШИ \t
# ЧТОБЫ СДЕЛАТЬ ЖИРНЫЙ ШРИФТ - ЗАКЛЮЧИ ТЕКСТ В ЗВЕЗДОЧКИ. ПРИМЕР: *жирный текст*
# ЧТОБЫ СДЕЛАТЬ КУРСИВНЫЙ ШРИФТ - ЗАКЛЮЧИ ТЕКСТ В ЗНАКИ ПОДЧЕРКИВАНИЯ. ПРИМЕР: _курсивный текст_
# ЧТОБЫ СДЕЛАТЬ ССЫЛКУ - НАПИШИ [inline URL](http://www.example.com/)
# УДАЧИ!!!

@bot.message_handler(func=lambda item: item.text == config.about[0], content_types=['text'])
def photo(message):
    bot.send_photo(message.chat.id, 'https://megaflowers.ru/pub/bouquet/vse-budet-horosho_m.jpg',
                   reply_markup=back_keyboard)

@bot.message_handler(func=lambda item: item.text == config.about[1], content_types=['text'])
def callbacks(message):
    bot.send_message(message.chat.id, '*Елена,12.09.2017*\
                     Санкт-Петербург/ 
                     «Начну  сразу со слов благодарности! За честь и порядочность, за добросовестно выполненный заказ, за оперативность и тактичность. Заказ был необычный, траурные цветы. Так случилось-потеряли мы близкого человека, подругу, дружба с которой связывала более 60 лет! И приехать проститься нет возможности. В интернете нашла прекрасно оформленный Ваш сайт, позвонила, Услышав приятный девичий голос я поняла- все сложится как я и хотела. С прекрасно оформленной большой корзиной роз мы смогли с Вашей помощью проститься с близким человеком, частички наших сердец были в тот момент рядом. Спасибо Вам большое!»_\
                     *Яна, 23.08.2017*/
                     Ростов-на-Дону/
                     _«Хочется выразить огромную благодарность команде Флориссимо за оформление нашей свадьбы!) С первых минут общений появились уверенность, что ребята справляются с поставленной задачей, во Флориссимо самый большой выбор реквизита и большой опыт флористического украшения торжеств. Все наши идеи были воплощены на 100%. Прийдя в зал в день церемонии мы были  восторге от той красоты, которую создали для нас! Кроме того, процесс подготовки проходил легко и без срывов, ребята всегда были на связи и готовы были найти решение любой проблеме) спасибо Вам огромное, желаем дальнейшего развития, интересных проектов и благодарных клиентов)_
                     , reply_markup=back_keyboard)

@bot.message_handler(func=lambda item: item.text == config.about[2], content_types=['text'])
def company(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = (telebot.types.KeyboardButton(text) for text in config.company)
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, config.about[2], reply_markup=keyboard)

@bot.message_handler(func=lambda item: item.text == config.company[0], content_types=['text'])
def mass_media(message):
    bot.send_message(message.chat.id, '*ТАСС* [http://tass.ru/ekonomika/2718890\
                     * Интерфакс* [сhttp://www.interfax-russia.ru/view.asp?id=638555]\
                     * НТВ* [http://www.ntv.ru/novosti/1460176/]\
                     * РБК* [https://www.rbc.ru/business/13/03/2016/56e2bc339a794718b0cb830d]\
                     * АНРТ* [http://anrt.info/news/production/30413-rossiya-nesposobna-k-importozamescheniyu]', reply_markup=back_keyboard)

@bot.message_handler(func=lambda item: item.text == config.company[1], content_types=['text'])
def works(message):
    bot.send_photo(message.chat.id, 'https://megaflowers.ru/pub/bouquet/vse-budet-horosho_m.jpg',
                   reply_markup=back_keyboard)


@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[3], content_types=['text'])
def delivery(message):
    bot.send_message(message.chat.id, '	Мы осуществляем круглосуточную доставку цветов на дом и в офис по Ростову-на-Дону и области.\
                     *Доставка в праздничные дни*\
                     Если день праздничный, то стоимость доставки составит *400 рублей*.\
                      *Доставка в ночное время*\
                     Ночное время - это время с 24:01 до 5:59\
                     Стоимость доставки фиксированная - базовая стоимость *(300р)+100р= 400 рублей*.\
                     *Стоимость доставки в ближайшие города*\
                     Батайск *450р*;\
                     п. Рассвет *600р*;\
                     п. Солнечный *450р*;\
                     Аксай *400р*;\
                     Ростов-на-Дону *300р*;\
                     Чалтырь *450р*;\
                     Азов *800р*;\
                     Таганрог *1500р*;\
                     Старочеркасск *500р*;\
                     Новочеркасск *800р*;\
                     Шахты *1500р*;\
                     Доставка за город до 20 км. *750р*;\
                     Доставка по области 20-35 км. *950р*;\
                     Доставка по области 36-50 км. *1300р*;\
                     Доставка по области 51-75 км. *1800р*;\
                     Доставка по области 76-100 км. *2000р*;\
                     Доставка по области 101-150 км. *3000р*;\
                     Доставка по области 151-200км. *4000р*.\
                     * Доставка в точное время*\
                     Доставка *«Точно в срок»* - осуществляется именно в то время, которое Вы указываете при оформлении заказа _(например 8:50, курьер преподнесет букет именно в это время)_ - стоимость *500 рублей*.\
                     * Срочный заказ*\
                     Срочный заказ - до 3х часов оплачивается дополнительно - *300 рублей*.\
 ', reply_markup=back_keyboard)

@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[4], content_types=['text'])
def sales(message):
    bot.send_message(message.chat.id, ' *5%* - скидка для клиентов, заказавших в нашей мастерской 3 и более букетов!\
                      *7%* -  скидка для клиентов, заказавших в нашей мастерской 7 и более букетов! Так же Вы получаете бесплатно дополнительные услуги от цветочной мастерской Florissimo!\
                      *10%* - скидка для клиентов, заказавших в нашей мастерской 15 и более букетов! Так же для таких клиентов - дизайнерская открытка к каждому букету в подарок! И расширенный комплекс услуг!\
                      *15%* - индивидуальная скидка, предназначена для самых преданных клиентов! Решение о такой скидке коллектив цветочной мастерской Florissimo принимает на основании многих факторов и индивидуально в отношении каждого клиента! Вы тоже можете получить такую скидку, даря цветы своим близким!\

', reply_markup=back_keyboard)


@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[5], content_types=['text'])
def contacts(message):
    bot.send_message(message.chat.id, 'Связаться с нами Вы можете с 8:30  до 21:00 по телефонам:\
                     +7(863)294-36-34\
                     +7(863)296-36-34\
                     *Whatsapp*: 8(961)282-67-23\
                     *Email*: florissimo@mail.ru\
                     *Наши адреса и график работы:*\
                      Showroom Florissimo, БЦ «Лига Наций» г.Ростов-на-Дону, ул. Суворова, 91-1 этаж ( живые и стабилизированные цветы, сувениры и подарки): *ежедневно с 8:30 до 21:00*\
                      Магазин цветов, декора и интерьера. Свадебный офис ул. Красноармейская, 210 - 1 этаж (живые и стабилизированные цветы, керамика, стекло, сувениры и подарки): *ежедневно с 8:30 до 21:00*\
                     *Сайт, посвященный свадебному оформлению и декору*: [http://www.florissimo-wendding.ru]\
                       
', reply_markup=back_keyboard)




@bot.callback_query_handler(func=lambda query: query.data)
def something_else(message):
    bot.send_message(message.chat.id, config.error_category, reply_markup=back_keyboard)



# @bot.message_handler(content_types=['photo'])
# def add_speaker_photo(message):
#     print(message.photo[0].file_id)

if __name__ == '__main__':
    main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = (telebot.types.KeyboardButton(text=button_text) for button_text in config.main_menu_keyboard
               if config.main_menu_keyboard.index(button_text) < 6)
    main_menu_keyboard.add(*buttons)

    back_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back_keyboard.add(telebot.types.KeyboardButton(text=config.back_button))

    hidden_keyboard = telebot.types.ReplyKeyboardRemove()

    bot.polling(none_stop=True)


