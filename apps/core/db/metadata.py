# -*- coding: utf-8 -*-

from decimal import Decimal

from django.db import models
from django.utils.encoding import force_text


class ISouthSupport(object):
    """
        Base interface object to support south migrations
        Ref.: http://south.aeracode.org/docs/customfields.html#south-field-triple
    """
    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = self.__class__.__module__ + '.' + self.__class__.__name__
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class BoolField(models.BooleanField, ISouthSupport):
    def __init__(self, *args, **kwargs):
        # South support: for this custom field type, default is managed by
        # db_type definition
        self._suppress_default = True
        models.BooleanField.__init__(self, *args, **kwargs)

    def db_type(self, connection):
        default = self.get_default()
        def_value = "DEFAULT 'S'" if default else "DEFAULT 'N'"
        field_name = self.db_column if self.db_column else self.name
        field_name = connection.ops.quote_name(field_name)
        sql = "CHAR(1) %s NOT NULL CHECK (%s IN ('S','N'))" % (def_value, field_name)
        return sql

    def get_prep_value(self, value):
        if value:
            return u'S'
        return u'N'

    def from_db_value(self, value, expression, connection, context):
        if isinstance(value, str):
            if value.strip() == 'S':
                return True
            return False
        return value


class AlphaField(models.Field, ISouthSupport):
    """
        Representation of CHAR data type of firebird.
        Native CharField is equal to Varchar
    """

    # __metaclass__ = models.SubfieldBase
    # Eliminado en Django 1.10

    def __init__(self, *args, **kwargs):
        self.max_length = kwargs['max_length']
        super(AlphaField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'CHAR(%s)' % self.max_length

    def get_prep_value(self, value):
        if value:
            return value.strip()
        return value

    def to_python(self, value):
        if isinstance(value, str):
            return value.strip()
        return value


class MoneyField(models.DecimalField, ISouthSupport):
    # __metaclass__ = models.SubfieldBase
    # Eliminado en Django 1.10

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs['max_digits'] = 18
        kwargs['decimal_places'] = 2
        kwargs['default'] = Decimal('0.00')
        super(MoneyField, self).__init__(verbose_name, name, **kwargs)
