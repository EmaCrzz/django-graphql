# -*- coding: utf-8 -*-

import re
import unicodedata
import json
import sys

from decimal import Decimal
from datetime import date
from collections import namedtuple

from django.template.base import Template, RequestContext
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, InvalidPage, EmptyPage


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, date):
            return obj.strftime('%d/%m/%Y')
        return json.JSONEncoder.default(self, obj)


def clean_null(value):
    if value in ['', 'NULL']:
        return None
    return value


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value in ('S', 'on',):
        return True
    elif value in ('N', 'off',):
        return False
    else:
        return None


def str_has_numbers(value):
    reg = re.search(r'[0-9]+', value)
    return reg is not None


def normalize_str(value):
    return unicodedata.normalize('NFKD', value).encode('ASCII', 'ignore')


def ms_from_timedelta(td):
    """
    Given a timedelta object, returns a float representing milliseconds
    """
    return (td.seconds * 1000) + (td.microseconds / 1000.0)


def paginate(request, dataset, offset=25):
    skip = offset or 1
    paginator = Paginator(dataset, skip)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        data = paginator.page(page)
    except (EmptyPage, InvalidPage):
        data = paginator.page(paginator.num_pages)

    return data


def getEdad(birth, today=None):
    '''
    Funcion que calcula la edad de una persona, permite calcular a partir de la fecha de nacimiento
    y conocer la edad a una fecha determinada.
    '''
    today = today or date.today()
    if birth:
        years = ((today.year - birth.year - 1) + (1 if (today.month, today.day) >= (birth.month, birth.day) else 0))
        return years
    else:
        return 0


def get_namedtuple_choices(name, choices_tuple):
    """Factory function for quickly making a namedtuple suitable for use in a
    Django model as a choices attribute on a field. It will preserve order.

    Usage::

        class MyModel(models.Model):
            COLORS = get_namedtuple_choices('COLORS', (
                (0, 'BLACK', 'Black'),
                (1, 'WHITE', 'White'),
            ))
            colors = models.PositiveIntegerField(choices=COLORS)

        >>> MyModel.COLORS.BLACK
        0
        >>> MyModel.COLORS.get_choices()
        [(0, 'Black'), (1, 'White')]

        class OtherModel(models.Model):
            GRADES = get_namedtuple_choices('GRADES', (
                ('FR', 'FR', 'Freshman'),
                ('SR', 'SR', 'Senior'),
            ))
            grade = models.CharField(max_length=2, choices=GRADES.get_choices())

        >>> OtherModel.GRADES.FR
        'FR'
        >>> OtherModel.GRADES.get_choices()
        [('FR', 'Freshman'), ('SR', 'Senior')]
    """

    class Choices(namedtuple(name, [name for val, name, desc in choices_tuple])):
        __slots__ = ()
        _choices = tuple([desc for val, name, desc in choices_tuple])

        def get_choices(self):
            return zip(tuple(self), self._choices)

    return Choices._make([val for val, name, desc in choices_tuple])


def render_string(request, value, context=None):
    html = mark_safe(value)
    t = Template(html)
    c = RequestContext(request)
    if context:
        c.update(context)
    return t.render(c)


def tuple_remove(original_tuple, elements_to_remove):
    lst = [item for item in original_tuple if item not in elements_to_remove]
    return tuple(lst)


def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Print iterations progress
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()
