# -*- coding: utf-8 -*-

import xlrd
from datetime import datetime
from config import dates

def table(day='20 ноября'):
    """
    Вывод расписания из таблицы
    :param day: день расписания
    :return: строка расписания за день 'day'
    """
    rb = xlrd.open_workbook('table.xls', formatting_info=True)
    res = '*' + day + '*\n\n'
    sheet = rb.sheet_by_index(dates.index(day))
    for rownum in range(sheet.nrows-2):
        row = sheet.row_values(rownum+2)
        res += '*' + row[0] + '*\n' + row[1] + '\n_' + row[2] + '_\n'
        if row[3]:
            res += '`' + row[3] + '`\n\n'
        else:
            res += '\n'
    return res


def flowers():
    """
    создание списка цветов из таблицы
    :return: список цветов
    """
    res = []
    rb = xlrd.open_workbook('speakers.xls', formatting_info=True)
    sheet = rb.sheet_by_index(dates.index(day))
    for rownum in range(sheet.nrows-1):
        row = sheet.row_values(rownum+1)
        res.append((row[0], row[1], row[2]))
    return res

def deputates():
    """
    создание списка спикеров из таблицы
    :param param: день расписания/депутаты
    :return: список спикеров/депутатов
    """
    res = []
    rb = xlrd.open_workbook('deputates.xls', formatting_info=True)
    sheet = rb.sheet_by_index(0)
    for rownum in range(sheet.nrows-1):
        row = sheet.row_values(rownum+1)
        if row[0]:
            res.append([row[0], (row[1], row[2])])
        else:
            res[len(res)-1].append((row[1], row[2]))
    return res

def volonteers():
    """
    Вывод команд и волонтеров из таблицы
    :return: номер команды, команда и контакты волонтера
    """
    rb = xlrd.open_workbook('volonteers.xls', formatting_info=True)
    res = ''
    sheet = rb.sheet_by_index(0)
    for rownum in range(sheet.nrows - 2):
        row = sheet.row_values(rownum + 1)
        res += str(rownum+1) + '. <b>' + row[0] + '</b>\n<i>' + row[1] + '</i>\n\n<code>' + row[2] + '</code>\n\n'\
               '<a href="' + row[3] + '">' + row[3] + '</a>\n\n'
    return res

def now():
    """
    Вывод текущего события из таблицы
    :return: строка расписания - текущее событие
    """
    time = datetime.now().timetuple()
    time = str(time[3]) + ':' + str(time[4])
    day = str(time[2]) + 'ноября'
    flag = True
    res = '*Прямо сейчас*\n'
    try:
        rb = xlrd.open_workbook('table.xls', formatting_info=True)
        sheet = rb.sheet_by_index(dates.index(day))
    except:
        res += 'Ничего нет'
        return res
    for rownum in range(sheet.nrows - 2):
        row = sheet.row_values(rownum + 2)
        interval = row[0].split('-')
        if interval[0] <= time <= interval[1]:
            res += '*' + row[0] + '*' + ': ' + row[1] + '\n'
            flag = False
    if flag:
        res += 'Ничего нет'
    return res


