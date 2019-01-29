# Models
# -*- coding: utf-8 -*-

from django.db import models

from apps.core import consts
# from apps.core.db import metadata
from apps.core.models import Localidad
from apps.personas.models import Persona

from .managers import EfectorManager


class EfectorTipo(models.Model):
    efe_tipo_id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=4, null=False, db_column='cod_efe_tipo')
    descripcion = models.CharField(max_length=50, null=False, db_column='desc_efe_tipo')

    class Meta:
        db_table = 'efector_tipo'
        verbose_name_plural = 'Tipos efectores'

    def __str__(self):
        return self.descripcion


class EfectorClasif(models.Model):
    efe_clasif_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, null=False, db_column='desc_efe_clasif')

    class Meta:
        db_table = 'efector_clasif'
        verbose_name_plural = 'Clasificacion efectores'

    def __str__(self):
        return self.descripcion


class Efector(Persona):
    efe_id = models.AutoField(primary_key=True)
    persona = models.OneToOneField(Persona, parent_link=True, db_column='per_id', related_name='efectores')
    cuie = models.CharField(max_length=6, null=True, blank=True)
    clasif = models.ForeignKey(EfectorClasif, null=True, blank=True, db_column='efe_clasif_id', related_name='efectores')
    localidad = models.ForeignKey(Localidad, null=True, blank=True, db_column='loc_id', related_name='efectores', on_delete=models.PROTECT)
    nota = models.CharField(max_length=200, null=True, blank=True)
    fec_upd = models.DateTimeField(null=False, blank=False, auto_now=True)

    objects = models.Manager()
    integrantes = EfectorManager()

    class Meta:
        db_table = 'efector'
        verbose_name_plural = 'Efectores'
        permissions = (
            ('view_efector', 'Can view efector'),
            ('edit_efector', 'Can edit efector'),
            ('modify_efector', 'Can modify efector'),
            ('manage_efector', 'Can manage efector')
        )

    def __str__(self):
        if not self.pk:
            return ''
        return ('%s - %s') % (self.cuie, self.razon_social)

    def save(self, *args, **kwargs):
        if self.efe_tipo_id == consts.EFE_TIPO_INST:
            self.integrante = False
        self.efe_nombre = self.razon_social
        self.tipo_id = consts.PER_JURIDICA
        super(Efector, self).save(*args, **kwargs)

    def _get_loc_provincia(self):
        if self.localidad_id:
            return '%s - %s' % (self.localidad.desc_loc, self.localidad.departamento.desc_dep)
        return ''
    loc_provincia = property(_get_loc_provincia)

    def _get_efe_full_name(self):
        if self.localidad_id:
            return '%s  (%s-%s)' % (self.razon_social, self.localidad.desc_loc, self.localidad.departamento.desc_dep)
        return self.razon_social
    efe_full_name = property(_get_efe_full_name)

    def as_dict(self):
        data = {
            'efe_id': self.pk,
            'cuie': self.cuie,
            'razon_social': self.razon_social,
            'localidad': '',
            'departamento': ''
        }
        if self.localidad_id:
            data['localidad'] = self.localidad.desc_loc
            data['departamento'] = self.localidad.departamento.desc_dep
        return data

    @property
    def description(self):
        tmpl = '[%(cuie)s] %(razon_social)s'
        if self.localidad_id:
            tmpl += ' (%(localidad)s - %(departamento)s)'
        return tmpl % self.as_dict()

    @property
    def has_predet_dom(self):
        has_predet_dom = self.domicilios.filter(predeterminado=True).exists()
        return has_predet_dom

    def get_localidad(self):
        if self.has_predet_dom:
            return self.domicilios.filter(predeterminado=True)[0].localidad.desc_loc
        return ''

    def get_departamento(self):
        if self.has_predet_dom:
            localidad = self.domicilios.filter(predeterminado=True)[0].localidad
            if localidad.departamento_id:
                return localidad.departamento.desc_dep
        return ''

    @staticmethod
    def is_cuie(value):
        if not value:
            return False
        if len(value) > 6:
            return False
        if (value[0] in ['e', 'E']) and (value[1:].isdigit()):
            return True
        elif value.isdigit():
            return True
        else:
            return False
