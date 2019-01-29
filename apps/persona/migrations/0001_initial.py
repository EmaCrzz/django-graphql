# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-23 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerBlackList',
            fields=[
                ('per_blacklist_id', models.AutoField(primary_key=True, serialize=False)),
                ('bad_pattern', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name_plural': 'Personas BlackList',
                'db_table': 'per_blacklist',
            },
        ),
        migrations.CreateModel(
            name='PerDom',
            fields=[
                ('per_dom_id', models.AutoField(primary_key=True, serialize=False)),
                ('calle', models.CharField(max_length=50)),
                ('nro_puerta', models.CharField(max_length=5)),
                ('piso', models.CharField(blank=True, max_length=2, null=True)),
                ('dpto', models.CharField(blank=True, max_length=3, null=True)),
                ('mzna', models.CharField(blank=True, max_length=3, null=True)),
                ('lote', models.CharField(blank=True, max_length=3, null=True)),
                ('entre_calle', models.CharField(blank=True, max_length=50, null=True)),
                ('y_calle', models.CharField(blank=True, max_length=50, null=True)),
                ('cpa', models.CharField(blank=True, max_length=10, null=True)),
                ('barrio', models.CharField(blank=True, max_length=40, null=True)),
                ('observaciones', models.CharField(blank=True, max_length=200, null=True)),
                ('predeterminado', models.BooleanField(default=False)),
                ('localidad', models.ForeignKey(db_column='loc_id', on_delete=django.db.models.deletion.PROTECT, to='core.Localidad')),
                ('municipio', models.ForeignKey(db_column='mun_id', on_delete=django.db.models.deletion.PROTECT, to='core.Municipio')),
            ],
            options={
                'verbose_name_plural': 'Domicilios',
                'db_table': 'per_domicilio',
                'permissions': (('view_perdom', 'Can view perdom'),),
            },
        ),
        migrations.CreateModel(
            name='PerEmail',
            fields=[
                ('per_email_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('observaciones', models.CharField(blank=True, max_length=200, null=True)),
                ('predeterminado', models.BooleanField(default=False)),
                ('email_clasif', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.EmailClasif')),
            ],
            options={
                'verbose_name_plural': 'Email',
                'db_table': 'per_email',
                'permissions': (('view_peremail', 'Can view peremail'),),
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('per_id', models.AutoField(primary_key=True, serialize=False)),
                ('apellido', models.CharField(blank=True, max_length=50, null=True)),
                ('nombre', models.CharField(blank=True, max_length=60, null=True)),
                ('nro_doc', models.IntegerField(blank=True, null=True)),
                ('fec_nac', models.DateField(blank=True, null=True)),
                ('full_name', models.CharField(blank=True, editable=False, max_length=200, null=True)),
                ('apellido_materno', models.CharField(blank=True, max_length=50, null=True)),
                ('razon_social', models.CharField(max_length=200)),
                ('cuit', models.CharField(blank=True, max_length=20, null=True)),
                ('cond_iva', models.ForeignKey(blank=True, db_column='cond_iva_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personas', to='core.CondIva')),
                ('doc_tipo', models.ForeignKey(blank=True, db_column='doc_tipo_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personas', to='core.DocTipo')),
                ('sexo', models.ForeignKey(db_column='sexo_id', on_delete=django.db.models.deletion.CASCADE, related_name='personas', to='core.Sexo')),
            ],
            options={
                'verbose_name_plural': 'Personas',
                'db_table': 'persona',
                'permissions': (('view_persona', 'Can view persona'), ('readonly_persona', 'Can view persona readonly')),
            },
        ),
        migrations.CreateModel(
            name='PersonaTipo',
            fields=[
                ('per_tipo_id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'persona_tipo',
            },
        ),
        migrations.CreateModel(
            name='PerTel',
            fields=[
                ('per_tel_id', models.AutoField(primary_key=True, serialize=False)),
                ('cod_pais', models.CharField(max_length=6)),
                ('cod_area', models.CharField(max_length=6)),
                ('nro_tel', models.CharField(max_length=15)),
                ('full_nro_tel', models.CharField(editable=False, max_length=20)),
                ('observaciones', models.CharField(blank=True, max_length=200, null=True)),
                ('predeterminado', models.BooleanField(default=False)),
                ('persona', models.ForeignKey(db_column='per_id', on_delete=django.db.models.deletion.CASCADE, related_name='telefonos', to='persona.Persona')),
                ('tel_clasif', models.ForeignKey(db_column='tel_clasif_id', on_delete=django.db.models.deletion.PROTECT, to='core.TelClasif')),
                ('tel_tipo', models.ForeignKey(db_column='tel_tipo_id', on_delete=django.db.models.deletion.PROTECT, to='core.TelTipo')),
            ],
            options={
                'verbose_name_plural': 'Telefonos',
                'db_table': 'per_telefono',
                'permissions': (('view_pertel', 'Can view pertel'),),
            },
        ),
        migrations.AddField(
            model_name='persona',
            name='tipo',
            field=models.ForeignKey(db_column='per_tipo_id', on_delete=django.db.models.deletion.CASCADE, related_name='personas', to='persona.PersonaTipo'),
        ),
        migrations.AddField(
            model_name='peremail',
            name='persona',
            field=models.ForeignKey(db_column='per_id', on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='persona.Persona'),
        ),
        migrations.AddField(
            model_name='perdom',
            name='persona',
            field=models.ForeignKey(db_column='per_id', on_delete=django.db.models.deletion.CASCADE, related_name='domicilios', to='persona.Persona'),
        ),
    ]
