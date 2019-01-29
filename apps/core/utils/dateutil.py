# -*- coding: utf-8 -*-

import calendar
import datetime


def str_to_date(value, format='%d/%m/%Y'):
    if value:
        if isinstance(value, basestring):
            result = datetime.datetime.strptime(value, format)
            return result.date()
        elif isinstance(value, datetime.date):
            return value
    return None


def periodo_to_date(periodo):
    """
    Dado un periodo (como string) de la forma mm/aaaa, devuelve una fecha
    como objeto date con el día fijado como 1 del mes.
    Ej:
    periodo = '05/2012'  ==>  date(2012, 5, 1)
    """
    if periodo:
        return str_to_date('01/' + periodo)
    return None


def date_to_periodo(value, format='%m/%Y'):
    """
        Dado un value de tipo date, devulve un dato con formato de
        periodo mes/año
    """
    return value.strftime(format)


def first_date_of_month(value):
    """
        Dada una fecha (value) de tipo date devuelve el primer día
        del mes de la fecha dada.
        Ej:
        value = date(2012, 5, 15)  ==>  date(2012, 5, 1)
    """
    fecha = value
    if isinstance(fecha, datetime.datetime):
        fecha = value.date()
    return datetime.date(fecha.year, fecha.month, 1)


def last_date_of_month(value):
    """
    Dado una fecha (value) devuelve el último día del mes de la fecha dada.
    Ej:
    value = date(2012, 5, 15)  ==>  date(2012, 5, 31)
    """
    day = calendar.mdays[value.month]
    if (day == 28) and calendar.isleap(value.year):
        day = 29
    return datetime.date(value.year, value.month, day)


def days_between(fecha1, fecha2):
    if fecha2 > fecha1:
        dif = fecha2 - fecha1
    else:
        dif = fecha1 - fecha2
    return dif.days


def inc_month(value, delta=30.5):
    fecha = value
    if isinstance(fecha, datetime.datetime):
        fecha = value.date()

    if delta:
        return value + datetime.timedelta(days=delta)

    month = fecha.month
    year = fecha.year
    month += 1
    if month > 12:
        month = 1
        year += 1
    return datetime.date(year, month, 1)


def dec_month(value, delta=30.5):
    fecha = value
    if isinstance(fecha, datetime.datetime):
        fecha = value.date()

    if delta:
        return value - datetime.timedelta(days=delta)

    month = fecha.month
    year = fecha.year
    month = month - 1
    if month < 1:
        month = 12
        year = year - 1
    return datetime.date(year, month, 1)
