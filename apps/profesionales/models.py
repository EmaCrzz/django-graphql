#  Models
# -*- coding: utf-8 -*-

from django.db import models

from apps.core import consts
from apps.persona.models import Persona


class Especialidad(models.Model):
    esp_id = models.AutoField(primary_key=True)
    desc_esp = models.CharField(max_length=50)

    class Meta:
        db_table = 'especialidad'
        verbose_name_plural = 'Especialidades'

    def __unicode__(self):
        return self.desc_esp


class Profesion(models.Model):
    profesion_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        db_table = 'profesion'
        verbose_name_plural = 'Profesiones'

    def __unicode__(self):
        return self.descripcion


class ProfesionalClasif(models.Model):
    prof_clasif_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        db_table = 'profesional_clasif'

    def __unicode__(self):
        return self.descripcion


class Profesional(Persona):
    prof_id = models.AutoField(primary_key=True)
    persona = models.OneToOneField(Persona, parent_link=True, db_column='per_id', related_name='profesionales')
    nro_matricula = models.CharField(max_length=8, null=True, blank=True)
    especialidad = models.ForeignKey(Especialidad, null=True, blank=True, db_column='esp_id', related_name='profesionales')
    clasificacion = models.ForeignKey(ProfesionalClasif, null=True, blank=True, db_column='prof_clasif_id', related_name='profesionales')

    class Meta:
        db_table = 'profesional'
        verbose_name_plural = 'Profesionales'
        permissions = (
            ('manage_profesional', 'Can manage profesional'),
            ('view_profesional', 'Can view profesional'),
            ('readonly_profesional', 'Can view profesional readonly')
        )

    def __unicode__(self):
        return u'%s' % self.full_name

    def save(self, *args, **kwargs):
        print('metodo save de profesional')
        self.tipo_id = consts.PER_FISICA
        super(Profesional, self).save(*args, **kwargs)


class ProfesionalMatricula(models.Model):
    TIPO_MATRICULA = (
        ('N', 'Nacional'),
        ('P', 'Provincial'),
    )
    prof_mat_id = models.AutoField(primary_key=True)
    profesional = models.ForeignKey(
        Profesional, null=False, blank=False, on_delete=models.CASCADE, db_column='prof_id', related_name='matriculas'
    )
    tipo = models.CharField(max_length=1, null=False, blank=False, choices=TIPO_MATRICULA)
    matricula = models.CharField(max_length=20, null=False, blank=False)
    fecha = models.DateField(null=True, blank=True, verbose_name='Fecha de matriculación')
    profesion = models.ForeignKey(
        Profesion, null=True, blank=True, on_delete=models.PROTECT, db_column='profesion_id'
    )
    especialidad = models.ForeignKey(Especialidad, null=False, blank=False, on_delete=models.PROTECT, db_column='esp_id')

    class Meta:
        db_table = 'profesional_matricula'
