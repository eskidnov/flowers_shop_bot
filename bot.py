# -*- coding: utf-8 -*-

import telebot
import config
import utils
import time
from catalog import hash
from config import catalog as cat
from database_communication import append_request
import importlib
import logging
import cherrypy


WEBHOOK_HOST = '195.133.1.136'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

bot = telebot.TeleBot(config.token)



# Наш вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)







@bot.message_handler(commands=['start'])
def start(message):
    importlib.reload(config)
    utils.del_user_basket(message.from_user.id)
    utils.set_basket(message.from_user.id)
    logging.info('Бот запущен пользователем', message.from_user.id)
    bot.send_message(message.chat.id, config.main_menu, parse_mode='markdown', reply_markup=main_menu_keyboard)


@bot.message_handler(commands=['help'])
def help(message):
    logging.info('Пользователь ' + str(message.from_user.id) + ' открыл список комманд')
    msg = '/start - запустить бота\n/help - отобразить список доступных команд'
    bot.send_message(message.chat.id, msg, parse_mode='markdown', reply_markup=hidden_keyboard)


@bot.message_handler(func=lambda item: item.text == config.back_button, content_types=['text'])
def back(message):
    """
    Возврат в меню (кнопка "Назад")
    :param message: Сообщение о нажатой кнопке
    """
    logging.info('Пользователь ' + str(message.from_user.id) + ' вернулся в основное меню')
    bot.send_message(message.chat.id, config.main_menu, reply_markup=main_menu_keyboard)


@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[0], content_types=['text'])
def catalog_button(message):
    """
    Обработка нажатия на кнопку "Наш каталог"
    :param message: Сообщение о нажатой кнопке
    """
    # cat - переменная catalog из config.py
    logging.info(str(cat.get_all_categories()))
    logging.info('Пользователь ' + str(message.from_user.id) + ' открыл "Наш каталог"')
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = (telebot.types.InlineKeyboardButton(text=button_text.item, callback_data=str(hash(button_text.item)))
               for button_text in cat.categories)
    keyboard.add(*buttons)

    bot.send_message(chat_id, config.main_menu_keyboard[0], reply_markup=back_keyboard, parse_mode='Markdown')
    bot.send_message(chat_id, 'Выберите категорию', reply_markup=keyboard, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda query: query.data in cat.get_all_categories())
def catalog(query):
    category = cat.find(query.data)
    logging.info(str(category))
    bot.answer_callback_query(query.id)
    logging.info('Пользователь ' + str(query.from_user.id) + ' открыл' + str(category.item))
    if isinstance(category.categories[0].categories[0], str):
        for item in category.categories:
            keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(telebot.types.InlineKeyboardButton(text=config.add_to_basket,
                                                            callback_data=config.add_to_basket+'_'+str(hash(item.item))))
            bot.send_message(query.message.chat.id, '*' + item.item + '*', reply_markup=back_keyboard,
                             parse_mode='Markdown')
            try:
            	bot.send_photo(query.message.chat.id, caption=item.categories[0], photo=item.categories[1],
                           reply_markup=keyboard)
            except telebot.apihelper.ApiException as ex:
                print ("err pic not found on ", item.categories[1])
                bot.send_message(query.message.chat.id, "err: pic not found", reply_markup=back_keyboard, parse_mode='Markdown')
               
    else:
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        buttons = (telebot.types.InlineKeyboardButton(text=subcat.item, callback_data=str(hash(subcat.item)))
                   for subcat in category.categories)
        keyboard.add(*buttons)

        bot.delete_message(query.message.chat.id, query.message.message_id - 1)
        bot.delete_message(query.message.chat.id, query.message.message_id)
        bot.send_message(query.message.chat.id, '*'+category.item+'*', reply_markup=back_keyboard, parse_mode='Markdown')
        bot.send_message(query.message.chat.id, 'Выберите нужный вам пункт меню', reply_markup=keyboard)



@bot.callback_query_handler(func=lambda query: config.add_to_basket in query.data)
def add_to_basket(query):
    logging.info(str(query.data))
    item = cat.find(query.data.split('_')[1])
    if not utils.get_basket(query.from_user.id):
        utils.set_basket(query.from_user.id)
    utils.add_to_basket(query.from_user.id, str(hash(item.item)))
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
            if (product):
                bot.send_message(message.chat.id, '*'+product.item+'*', parse_mode='Markdown')
                bot.send_photo(message.chat.id, caption=product.categories[0], photo=product.categories[1])
            else:
                bot.send_message(message.chat.id, 'База данных товаров обновилась! Похоже, некоторых товаров из вашей корзины больше нет...')
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
        price = 0
        for item in user_basket:
            item_price = cat.find(item).categories[0].split('\n')[-1]
            res += cat.find(item).item + ' - ' + item_price + ' руб.\n'
            price += int(item_price)
        # bot.send_message(message.chat.id, res, parse_mode='Markdown', reply_markup=keyboard)

        bot.send_invoice(chat_id=message.chat.id,
                         title=config.user_basket,
                         description=res,
                         invoice_payload='invoice',
                         provider_token=config.provider_token,
                         start_parameter='invoice',
                         currency='rub',
                         prices=[telebot.types.LabeledPrice(label=config.user_basket, amount=price*100)],
                         need_name=True,
                         need_email=True,
                         need_phone_number=True,
                         need_shipping_address=True,
                         is_flexible=True,
                         reply_markup=keyboard)
    else:
        bot.send_message(chat_id=message.chat.id, text=config.empty_basket)


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    bot.answer_shipping_query(shipping_query_id=shipping_query.id,
                              ok=True,
                              shipping_options=config.shipping_options,
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
        buys_list += cat.find(item).item + '\n'
    append_request(order_info.name, order_info.email, order_info.phone_number, order_info.shipping_address,
                   buys_list, message.successful_payment.total_amount / 100, '')

    utils.del_user_basket(message.from_user.id)


@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[2], content_types=['text'])
def about(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = (telebot.types.KeyboardButton(text) for text in config.about)
    keyboard.add(*buttons)
    keyboard.add(telebot.types.KeyboardButton(text=config.back_button))
    bot.send_message(message.chat.id, config.main_menu_keyboard[2], reply_markup=keyboard)


@bot.message_handler(func=lambda item: item.text == config.about[0], content_types=['text'])
def photo(message):
    for item in config.photos:
        bot.send_photo(message.chat.id, item, reply_markup=back_keyboard)
    bot.send_message(message.chat.id, '*Больше фото доставок можно найти на нашем сайте:* '\
                                      'http://www.florissimo-shop.ru/getflower.html?page=1', parse_mode='Markdown',
                     disable_web_page_preview=True)


@bot.message_handler(func=lambda item: item.text == config.about[1], content_types=['text'])
def callbacks(message):
    for item in config.reviews:
        bot.send_message(message.chat.id, item, reply_markup=back_keyboard, parse_mode='Markdown',
                         disable_web_page_preview=True)


@bot.message_handler(func=lambda item: item.text == config.about[2], content_types=['text'])
def company(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = (telebot.types.KeyboardButton(text) for text in config.company)
    keyboard.add(*buttons)
    keyboard.add(telebot.types.KeyboardButton(text=config.back_button))
    bot.send_message(message.chat.id, config.about[2], reply_markup=keyboard)
    bot.send_message(message.chat.id, config.company_info, disable_web_page_preview=True, parse_mode='Markdown')


@bot.message_handler(func=lambda item: item.text == config.company[0], content_types=['text'])
def mass_media(message):
    for item in config.mass_media:
        bot.send_message(message.chat.id, item, reply_markup=back_keyboard, parse_mode='Markdown')


@bot.message_handler(func=lambda item: item.text == config.company[1], content_types=['text'])
def works(message):
    bot.send_message(message.chat.id, '*Красно-пурпурная свадьба в Усадьбе*', parse_mode='Markdown')
    for item in config.works:
        bot.send_photo(message.chat.id, item, reply_markup=back_keyboard)
    bot.send_message(message.chat.id, '*Больше фото и видео наших работ можно найти на нашем сайте:* '\
                                      'http://www.florissimo-shop.ru/portfolio.html', parse_mode='Markdown',
                     disable_web_page_preview=True)


@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[3], content_types=['text'])
def delivery(message):
    for item in config.delivery:
        bot.send_message(message.chat.id, item, reply_markup=back_keyboard, parse_mode='Markdown')


@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[4], content_types=['text'])
def sales(message):
    for item in config.sales:
        bot.send_message(message.chat.id, item, reply_markup=back_keyboard, parse_mode='Markdown')


@bot.message_handler(func=lambda item: item.text == config.main_menu_keyboard[5], content_types=['text'])
def contacts(message):
    for item in config.contacts:
        bot.send_message(message.chat.id, item, reply_markup=back_keyboard, parse_mode='Markdown',
                         disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda query: query.data)
def something_else(query):
    bot.answer_callback_query(query.id)
    bot.send_message(query.message.chat.id, config.error_category, reply_markup=back_keyboard)


@bot.message_handler(content_types=['photo'])
def add_speaker_photo(message):
    bot.send_message(message.chat.id, message.photo[0].file_id)


if __name__ == '__main__':

    main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = (telebot.types.KeyboardButton(text=button_text) for button_text in config.main_menu_keyboard
               if config.main_menu_keyboard.index(button_text) < 6)
    main_menu_keyboard.add(*buttons)

    back_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back_keyboard.add(telebot.types.KeyboardButton(text=config.back_button))

    hidden_keyboard = telebot.types.ReplyKeyboardRemove()




    # Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
    bot.remove_webhook()

    # Ставим заново вебхук
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))

    # Указываем настройки сервера CherryPy
    cherrypy.config.update({
        'server.socket_host': WEBHOOK_LISTEN,
        'server.socket_port': WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': WEBHOOK_SSL_CERT,
        'server.ssl_private_key': WEBHOOK_SSL_PRIV
    })

    # Собственно, запуск!
    cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

    # while True:
    #     try:
    #         bot.polling(none_stop=True)
    #         logging.warn('polled')
    #     except (KeyboardInterrupt, SystemExit):
    #         break
    #     except Exception as err:
    #         logging.error(err)
    #         logging.error('Polling error')
    #         time.sleep(5)
    #         continue
    #     break



