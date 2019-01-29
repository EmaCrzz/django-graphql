# -*- coding: utf-8 -*-

from django.db import models

from .db import metadata


class DocClase(models.Model):
    doc_clase_id = models.SmallIntegerField(primary_key=True)
    cod_doc_clase = models.CharField(max_length=1, null=True, blank=True)
    desc_doc_clase = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'doc_clase'
        verbose_name_plural = 'Clases de Documentos'

    def __unicode__(self):
        return self.desc_doc_clase


class DocTipo(models.Model):
    doc_tipo_id = models.AutoField(primary_key=True)
    cod_doc_tipo = models.CharField(max_length=4, null=True, blank=True)
    desc_doc_tipo = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'doc_tipo'
        verbose_name_plural = 'Tipos de Documentos'

    def __unicode__(self):
        return self.desc_doc_tipo


class Sexo(models.Model):
    sexo_id = models.SmallIntegerField(primary_key=True)
    cod_sexo = models.CharField(max_length=1, null=False, blank=False)
    desc_sexo = models.CharField(max_length=15, null=False, blank=False)

    class Meta:
        db_table = 'sexo'
        verbose_name_plural = 'Sexos'

    def __unicode__(self):
        return self.desc_sexo


class Pais(models.Model):
    pais_id = models.AutoField(primary_key=True)
    desc_pais = models.CharField(max_length=50, null=False, blank=False)
    nacionalidad = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'pais'
        verbose_name_plural = 'Paises'

    def __unicode__(self):
        return self.desc_pais


class Provincia(models.Model):
    prov_id = models.AutoField(primary_key=True)
    cod_prov = models.CharField(max_length=2)
    desc_prov = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'provincia'
        verbose_name_plural = 'Provincias'

    def __unicode__(self):
        return self.desc_prov


class Departamento(models.Model):
    dep_id = models.AutoField(primary_key=True)
    provincia = models.ForeignKey(Provincia, null=False, db_column='prov_id', related_name='departamentos')
    cod_dep = models.CharField(max_length=3)
    desc_dep = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'departamento'
        verbose_name_plural = 'Departamentos'

    def __unicode__(self):
        return self.desc_dep


class Localidad(models.Model):
    loc_id = models.AutoField(primary_key=True)
    departamento = models.ForeignKey(Departamento, db_column='dep_id', related_name='localidades')
    cod_loc = models.CharField(max_length=3, null=True, blank=True)
    desc_loc = models.CharField(max_length=50, null=False, blank=False)
    cod_postal = models.IntegerField(null=True, blank=True)
    cod_siisa = models.CharField(max_length=20, null=True, blank=True)
    id_siisa = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'localidad'
        verbose_name_plural = 'Localidades'
        permissions = (("view_localidad", "Can view localidad"),)

    def __unicode__(self):
        return (u'%s') % (self.desc_loc)


class Municipio(models.Model):
    mun_id = models.AutoField(primary_key=True)
    localidad = models.ForeignKey(Localidad, db_column='loc_id', related_name='municipios', on_delete=models.PROTECT)
    desc_mun = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'municipio'
        verbose_name_plural = 'Municipios'

    def __unicode__(self):
        return (u'%s') % (self.desc_mun)


class Alfabetizacion(models.Model):
    alfab_id = models.AutoField(primary_key=True)
    cod_alfab = models.CharField(max_length=2, null=True, blank=True)
    nivel = models.CharField(max_length=40, null=False, blank=False)

    class Meta:
        db_table = 'alfabetizacion'
        verbose_name_plural = 'Alfabetizacion'

    def __unicode__(self):
        return self.nivel


class Tribu(models.Model):
    tribu_id = models.AutoField(primary_key=True)
    tribu_nombre = models.CharField(max_length=80, null=False, blank=False)

    class Meta:
        db_table = 'tribu'
        verbose_name_plural = 'Tribus'

    def __unicode__(self):
        return self.tribu_nombre


class Lengua(models.Model):
    lengua_id = models.AutoField(primary_key=True)
    lengua_desc = models.CharField(max_length=80, null=False, blank=False)

    class Meta:
        db_table = 'lengua'
        verbose_name_plural = 'Lenguas'

    def __unicode__(self):
        return self.lengua_desc


class Laboratorio(models.Model):
    lab_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, null=False, blank=False)

    class Meta:
        db_table = 'laboratorio'
        verbose_name_plural = 'Laboratorios'

    def __unicode__(self):
        return self.nombre


class UnidadMedida(models.Model):
    unid_med_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=35, null=False, blank=False, db_column='unid_med')
    abrev = models.CharField(max_length=5, null=True, blank=True, db_column='abrev')

    class Meta:
        db_table = 'unid_medida'
        verbose_name_plural = 'Unidades de Medida'

    def __unicode__(self):
        return self.nombre


class DiabetesTipo(models.Model):
    diab_tipo_id = models.AutoField(primary_key=True)
    diab_tipo_descr = models.CharField(max_length=30, null=False, blank=False)

    class Meta:
        db_table = 'diabetes_tipo'
        verbose_name_plural = 'Tipos de diabetes'

    def __unicode__(self):
        return self.diab_tipo_descr


class ScoreRCVClasif(models.Model):
    score_clasif_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, blank=False, null=False)
    descripcion = models.CharField(max_length=80, blank=True, null=True)
    color = models.CharField(max_length=7, null=True, blank=True)

    class Meta:
        db_table = 'score_rcv_clasif'
        verbose_name_plural = 'Clasificación de score riesgo cardiovascular'

    def __unicode__(self):
        return self.nombre


class ObraSocial(models.Model):
    obra_soc_id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=6, blank=True, null=True)
    nombre = models.CharField(max_length=200, blank=False, null=False)
    sigla = models.CharField(max_length=30, blank=True, null=True)
    vigente = metadata.BoolField(default=False)

    class Meta:
        db_table = 'obra_social'
        verbose_name_plural = 'Obras sociales'

    def __unicode__(self):
        return u'%s - %s' % (self.codigo, self.nombre,)


class EnteEducGestion(models.Model):  # estatal, privado, social/cooperativo
    ente_gestion_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, null=False, db_column='desc_ente_gestion')

    class Meta:
        db_table = 'ente_educ_gestion'
        verbose_name = 'Tipo de Gestión'
        verbose_name_plural = 'Tipos de Gestión'

    def __unicode__(self):
        return self.descripcion


class EnteEducNivel(models.Model):  # inicial,primario, ...
    ente_nivel_id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=4, null=False, db_column='cod_ente_nivel')
    descripcion = models.CharField(max_length=50, null=False, db_column='desc_ente_nivel')

    class Meta:
        db_table = 'ente_educ_nivel'
        verbose_name = 'Ente Educativo Nivel'
        verbose_name_plural = 'Entes Educativos Niveles'

    def __unicode__(self):
        return self.descripcion


class EnteEducClasif(models.Model):  # municipal o provincial nacional, etc
    ente_clasif_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, null=False, db_column='desc_ente_clasif')

    class Meta:
        db_table = 'ente_educ_clasif'
        verbose_name = 'Clasificación'
        verbose_name_plural = 'Entes Educativos Clasificaciones'

    def __unicode__(self):
        return self.descripcion


class EnteEducModalidad(models.Model):  # comun o especial
    ente_modalidad_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, null=False, db_column='desc_ente_modalidad')

    class Meta:
        db_table = 'ente_educ_modalidad'
        verbose_name = 'Ente Educativo Modalidad'
        verbose_name_plural = 'Entes Educativos Modalidades'

    def __unicode__(self):
        return self.descripcion


class EnteEducativo(models.Model):
    ente_educ_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    tipo_gestion = models.ForeignKey(EnteEducGestion, null=True, blank=True, db_column='gestion_id', related_name='entes_educ')
    nivel = models.ForeignKey(EnteEducNivel, null=True, blank=True, db_column='nivel_id', related_name='entes_educ')
    clasif = models.ForeignKey(EnteEducClasif, null=True, blank=True, db_column='clasif_id', related_name='entes_educ')
    modalidad = models.ForeignKey(EnteEducModalidad, null=True, blank=True, db_column='modalidad_id', related_name='entes_educ')
    domicilio = models.CharField(max_length=150, null=True, blank=True)
    localidad = models.ForeignKey(Localidad, null=True, blank=True)
    telefono = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    representante = models.CharField(max_length=100, null=True, blank=True)
    repr_telefono = models.CharField(max_length=150, null=True, blank=True)
    repr_email = models.EmailField(max_length=254, null=True, blank=True)
    rural = models.BooleanField(default=False)
    referente = models.CharField(max_length=100, null=True, blank=True)
    rural_plurigrado = models.BooleanField(default=False)
    intercultural_bilingue = models.BooleanField(default=False)
    cod_siisa = models.CharField(max_length=20, null=True, blank=True)
    id_siisa = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'ente_educativo'
        verbose_name = 'Ente educativo'
        verbose_name_plural = 'Entes Educativos'
        permissions = (("view_enteeducativo", "Can view Ente educativo"),)

    def __unicode__(self):
        return u'[%s]-%s' % (self.ente_educ_id, self.nombre,)


class TelClasif(models.Model):
    tel_clasif_id = models.AutoField(primary_key=True)
    clasificacion = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = 'tel_clasif'
        verbose_name = 'Clasificación Teléfono'
        verbose_name_plural = 'Clasificaciones Teléfono'

    def __unicode__(self):
        return self.clasificacion


class TelTipo(models.Model):
    tel_tipo_id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = 'tel_tipo'
        verbose_name = 'Tipo de Teléfono'
        verbose_name_plural = 'Tipos de Teléfono'

    def __unicode__(self):
        return self.tipo


class EmailClasif(models.Model):
    email_clasif_id = models.AutoField(primary_key=True)
    clasificacion = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = 'email_clasif'
        verbose_name = 'Clasificación Email'
        verbose_name_plural = 'Clasificaciones Email'

    def __unicode__(self):
        return self.clasificacion


class CondIva(models.Model):
    cond_iva_id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=3, null=False, blank=False)
    descripcion = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
            db_table = 'cond_iva'
            verbose_name = u'Condición frente a IVA'

    def __unicode__(self):
        return self.descripcion
