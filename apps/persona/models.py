# Models
# -*- coding: utf-8 -*-
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from django.db import models
from django.core.exceptions import ValidationError

from apps.core import consts
from apps.core.models import (
    DocTipo,
    EmailClasif,
    Localidad,
    Municipio,
    Sexo,
    TelClasif,
    TelTipo,
    CondIva
)


class PersonaTipo(models.Model):
    per_tipo_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = 'persona_tipo'

    def __srt__(self):
        return self.descripcion


class Persona(models.Model):
    per_id = models.AutoField(primary_key=True)
    apellido = models.CharField(max_length=50, null=True, blank=True)
    nombre = models.CharField(max_length=60, null=True, blank=True)
    nro_doc = models.IntegerField(null=True, blank=True)
    doc_tipo = models.ForeignKey(DocTipo, null=True, blank=True, db_column='doc_tipo_id', related_name='personas')
    sexo = models.ForeignKey(Sexo, null=False, blank=False, db_column='sexo_id', related_name='personas')
    fec_nac = models.DateField(null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True, editable=False)
    tipo = models.ForeignKey(PersonaTipo, null=False, blank=False, db_column='per_tipo_id', related_name='personas')
    apellido_materno = models.CharField(max_length=50, null=True, blank=True)
    razon_social = models.CharField(max_length=200, null=False, blank=False)
    cuit = models.CharField(max_length=20, null=True, blank=True)
    cond_iva = models.ForeignKey(CondIva, null=True, blank=True, db_column='cond_iva_id', related_name='personas')

    class Meta:
        db_table = 'persona'
        verbose_name_plural = 'Personas'
        permissions = (
            ('view_persona', 'Can view persona'),
            ('readonly_persona', 'Can view persona readonly')
        )

    def __unicode__(self):
        return self.razon_social

    def get_full_name(self):
        """
        Este método devuelve el campo full_name que contiene el apellido y
        el nombre normalizado.
        """
        return self.full_name

    def save(self, *args, **kwargs):
        if self.tipo_id == consts.PER_FISICA:
            print('metodo save de persona')
            if self.apellido:
                self.apellido = self.apellido.strip().upper()
            if not self.apellido:
                raise ValidationError('Apellido debe tener un valor.')
            if self.nombre:
                self.nombre = self.nombre.strip().upper()
            if not self.nombre:
                raise ValidationError('Nombre debe tener un valor.')
            if self.apellido_materno:
                if self.apellido_materno.strip():
                    self.apellido_materno = self.apellido_materno.strip().upper()
                else:
                    self.apellido_materno = None
            self.razon_social = u'%s %s' % (self.apellido, self.nombre)
        elif self.tipo_id == consts.PER_JURIDICA:
            if self.razon_social:
                self.razon_social = self.razon_social.strip().upper()
            if not self.razon_social:
                raise ValidationError('Razon Social debe tener un valor.')
            self.sexo_id = consts.SEXO_EMPRESA
        self.full_name = self.razon_social
        super(Persona, self).save(*args, **kwargs)


class PerDom(models.Model):
    per_dom_id = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, null=False, blank=False, db_column='per_id', on_delete=models.CASCADE, related_name='domicilios')
    calle = models.CharField(max_length=50, null=False, blank=False)
    nro_puerta = models.CharField(max_length=5, null=False, blank=False)
    piso = models.CharField(max_length=2, null=True, blank=True)
    dpto = models.CharField(max_length=3, null=True, blank=True)
    mzna = models.CharField(max_length=3, null=True, blank=True)
    lote = models.CharField(max_length=3, null=True, blank=True)
    entre_calle = models.CharField(max_length=50, null=True, blank=True)
    y_calle = models.CharField(max_length=50, null=True, blank=True)
    cpa = models.CharField(max_length=10, null=True, blank=True)
    localidad = models.ForeignKey(Localidad, null=False, blank=False, db_column='loc_id', on_delete=models.PROTECT)
    municipio = models.ForeignKey(Municipio, null=False, blank=False, db_column='mun_id', on_delete=models.PROTECT)
    barrio = models.CharField(max_length=40, null=True, blank=True)
    observaciones = models.CharField(max_length=200, null=True, blank=True)
    predeterminado = models.BooleanField(default=False)

    class Meta:
        db_table = 'per_domicilio'
        verbose_name_plural = 'Domicilios'
        permissions = (("view_perdom", "Can view perdom"),)

    def __unicode__(self):
        return u'[%s] - %s' % (self.persona, self.calle)


class PerTel(models.Model):
    per_tel_id = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, null=False, blank=False, db_column='per_id', on_delete=models.CASCADE, related_name='telefonos')
    tel_clasif = models.ForeignKey(TelClasif, null=False, blank=False, db_column='tel_clasif_id', on_delete=models.PROTECT)
    tel_tipo = models.ForeignKey(TelTipo, null=False, blank=False, db_column='tel_tipo_id', on_delete=models.PROTECT)
    cod_pais = models.CharField(max_length=6, null=False, blank=False)
    cod_area = models.CharField(max_length=6, null=False, blank=False)
    nro_tel = models.CharField(max_length=15, null=False, blank=False)
    full_nro_tel = models.CharField(max_length=20, null=False, blank=False, editable=False)
    observaciones = models.CharField(max_length=200, null=True, blank=True)
    predeterminado = models.BooleanField(default=False)

    class Meta:
        db_table = 'per_telefono'
        verbose_name_plural = 'Telefonos'
        permissions = (("view_pertel", "Can view pertel"),)

    def __unicode__(self):
        return u'[%s] - %s' % (self.persona, self.full_nro_tel)

    def save(self, *args, **kwargs):
        string_value = self.cod_pais + self.cod_area + self.nro_tel
        try:
            value = phonenumbers.parse(string_value, 'AR')
        except NumberParseException:
            raise ValidationError('Ingrese un numero de telefono con formato valido.')
        if phonenumbers.is_valid_number(value) and phonenumbers.is_possible_number(value):
            self.full_nro_tel = phonenumbers.format_number(value, phonenumbers.PhoneNumberFormat.E164)
        else:
            raise ValidationError('Ingrese un numero de telefono con formato valido.')
        super(PerTel, self).save(*args, **kwargs)


class PerEmail(models.Model):
    per_email_id = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, null=False, blank=False, db_column='per_id', on_delete=models.CASCADE, related_name='emails')
    email_clasif = models.ForeignKey(EmailClasif, null=False, blank=False, on_delete=models.PROTECT)
    email = models.EmailField(max_length=254, null=False, blank=False)
    observaciones = models.CharField(max_length=200, null=True, blank=True)
    predeterminado = models.BooleanField(default=False)

    class Meta:
        db_table = 'per_email'
        verbose_name_plural = 'Email'
        permissions = (("view_peremail", "Can view peremail"),)

    def __unicode__(self):
        return u'[%s] - %s' % (self.persona, self.email)


class PerBlackList(models.Model):
    """BlackList para patrones de texto de nombres y apellidos no permitidos"""
    per_blacklist_id = models.AutoField(primary_key=True)
    bad_pattern = models.CharField(max_length=60)

    class Meta:
        db_table = 'per_blacklist'
        verbose_name_plural = 'Personas BlackList'

    def __unicode__(self):
        return self.bad_pattern

    def save(self, *args, **kwargs):
        if self.bad_pattern:
            self.bad_pattern = self.bad_pattern.strip().upper()
        super(PerBlackList, self).save(*args, **kwargs)
