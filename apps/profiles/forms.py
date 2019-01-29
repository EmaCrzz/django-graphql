# -*- coding: utf-8 -*-

import copy
from datetime import datetime

from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.admin.models import ADDITION, CHANGE

from apps.audit.models import AuditLog
# from apps.nomencladores.models import PrestacionPaquete
from apps.efectores.models import Efector
from apps.qbuilder.models import Query, QueryUser

from .models import UsuarioEfector


class ProfileForm(forms.Form):
    first_name = forms.CharField(required=True, label='Nombre')
    last_name = forms.CharField(required=True, label='Apellido')
    email = forms.EmailField(required=False, label='E-Mail')

    def __init__(self, request, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.request = request

    def load(self, instance):
        """
        instance: es una instancia de UserProfile
        """
        user = instance.user
        self.data['first_name'] = user.first_name
        self.data['last_name'] = user.last_name
        self.data['email'] = user.email
        self.is_bound = True

    def save(self, commit=True):
        user = self.request.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        profile = user.profile
        profile.save()
        return profile


class UserForm(forms.Form):
    username = forms.CharField(required=True, label='Usuario')
    password1 = forms.CharField(required=False, label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(required=False, label="Confirmar contraseña", widget=forms.PasswordInput)
    first_name = forms.CharField(required=True, label='Nombre')
    last_name = forms.CharField(required=True, label='Apellido')
    email = forms.EmailField(required=False, label='E-Mail')
    efe_id = forms.Field(widget=forms.HiddenInput, required=False)
    institucion_id = forms.Field(widget=forms.HiddenInput, required=False)
    efector = forms.CharField(required=True, label='Efector')
    can_modify_nro_doc = forms.BooleanField(required=False, label=('Puede modificar número de documento'))
    activo = forms.BooleanField(required=False, label=('Activo'), initial=True)
    is_staff = forms.BooleanField(required=False, label=('Es staff'), initial=False)
    institucion = forms.CharField(required=True, label='Institución')

    def __init__(self, user, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.user = user

    def _create_user(self):
        """
        Crea un nuevo usuario en caso de alta
        """
        user = User()
        user.is_staff = False
        user.is_superuser = False
        return user

    def load(self, user):
        self.user = user
        self.data['username'] = user.username
        self.data['first_name'] = user.first_name
        self.data['last_name'] = user.last_name
        self.data['email'] = user.email
        efe_name = user.profile.efector.full_name
        efe_cuie = user.profile.efector.cuie
        if user.profile.efector.domicilios.exists():
            efe_loc = user.profile.efector.domicilios.last().localidad.desc_loc
            efe_depto = user.profile.efector.domicilios.last().localidad.departamento.desc_dep
            self.data['efector'] = '[%s] %s (%s - %s)' % (efe_cuie, efe_name, efe_loc, efe_depto)
        else:
            self.data['efector'] = '[%s] %s' % (efe_cuie, efe_name)
        self.data['efe_id'] = user.profile.efector_id
        # El siguiente control corrige la falta (inicial y momentánea) de asociaciones entre ususarios e instituciones
        if user.profile.institucion_id:
            inst_name = user.profile.institucion.full_name
            inst_cuie = user.profile.institucion.cuie
            if user.profile.institucion.domicilios.exists():
                inst_loc = user.profile.institucion.domicilios.last().localidad.desc_loc
                inst_depto = user.profile.institucion.domicilios.last().localidad.departamento.desc_dep
                self.data['institucion'] = '[%s] %s (%s - %s)' % (inst_cuie, inst_name, inst_loc, inst_depto)
            else:
                self.data['institucion'] = '[%s] %s' % (inst_cuie, inst_name)
            self.data['institucion_id'] = user.profile.institucion_id
        self.data['can_modify_nro_doc'] = user.has_perm('afiliados.modify_nro_doc')
        self.data['activo'] = user.is_active
        self.data['is_staff'] = user.is_staff
        self.is_bound = True

    def inserting(self):
        return False

    def save(self):
        action = CHANGE
        old_object = copy.deepcopy(self.user)
        if not self.user:
            action = ADDITION
            self.user = self._create_user()
            self.user.set_password(self.cleaned_data['password1'])
        if action == CHANGE:
            is_activo = self.user.is_active

        self.user.username = self.cleaned_data['username']
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']
        self.user.is_active = self.cleaned_data['activo']
        self.user.is_staff = self.cleaned_data['is_staff']
        self.user.save()
        if action == ADDITION:
            if self.user.is_active is True:
                self.user.last_login = self.user.date_joined
                self.user.save()
        if action == CHANGE:
            if is_activo is False and self.user.is_active is True:
                self.user.last_login = datetime.now()
                self.user.save()

        if self.cleaned_data['can_modify_nro_doc'] is not None:
            perm = Permission.objects.get(codename='modify_nro_doc')
            if self.cleaned_data['can_modify_nro_doc'] is True:
                self.user.user_permissions.add(perm)
            else:
                self.user.user_permissions.remove(perm)

        grupos = self.data.getlist('grupos')

        for grupo in grupos:
            try:
                grp = Group.objects.get(pk=grupo)
                self.user.groups.add(grp)
            except Group.DoesNotExist:
                pass

        user_groups = [g.pk for g in self.user.groups.all()]

        for grupo_usuario in user_groups:
            if not str(grupo_usuario) in grupos:
                grp = Group.objects.get(pk=grupo_usuario)
                self.user.groups.remove(grp)

        # paquetes = self.data.getlist('u_paquetes')

        # for paquete in paquetes:
        #     try:
        #         paq = PrestacionPaquete.objects.get(pk=paquete)
        #         try:
        #             up = UsuarioPrestacionPaquete.objects.get(usuario=self.user.profile.usuario, paquete=paq)
        #         except UsuarioPrestacionPaquete.DoesNotExist:
        #             usuario_paquete = UsuarioPrestacionPaquete()
        #             usuario_paquete.usuario = self.user.profile.usuario
        #             usuario_paquete.paquete = paq
        #             usuario_paquete.save()
        #     except PrestacionPaquete.DoesNotExist:
        #         pass

        # user_paquetes = [p.paquete.pk for p in self.user.profile.usuario.pre_paquetes.all()]

        # for paquete_usuario in user_paquetes:
        #     if not str(paquete_usuario) in paquetes:
        #         paq = PrestacionPaquete.objects.get(pk=paquete_usuario)
        #         up = UsuarioPrestacionPaquete.objects.get(usuario=self.user.profile.usuario, paquete=paq)
        #         up.delete()

        efectores = self.data.getlist('u_efectores')

        for efector in efectores:
            try:
                efe = Efector.objects.get(pk=efector)
                try:
                    ue = UsuarioEfector.objects.get(usuario=self.user.profile.usuario, efector=efe)
                except UsuarioEfector.DoesNotExist:
                    usuario_efector = UsuarioEfector()
                    usuario_efector.usuario = self.user.profile.usuario
                    usuario_efector.efector = efe
                    usuario_efector.save()
            except Efector.DoesNotExist:
                pass

        user_efectores = [e.efector.pk for e in self.user.profile.usuario.efectores.all()]

        for efector_usuario in user_efectores:
            if not str(efector_usuario) in efectores:
                efe = Efector.objects.get(pk=efector_usuario)
                ue = UsuarioEfector.objects.get(usuario=self.user.profile.usuario, efector=efe)
                ue.delete()

        queries = self.data.getlist('u_queries')

        for query in queries:
            try:
                que = Query.objects.get(pk=query, activo='S')
                try:
                    uq = QueryUser.objects.get(user=self.user, qry=que)
                except QueryUser.DoesNotExist:
                    usuario_query = QueryUser()
                    usuario_query.user = self.user
                    usuario_query.qry = que
                    usuario_query.save()
            except Query.DoesNotExist:
                pass

        user_queries = [q.pk for q in self.user.queries.filter(activo='S')]

        for query_usuario in user_queries:
            if not str(query_usuario) in queries:
                que = Query.objects.get(pk=query_usuario, activo='S')
                uq = QueryUser.objects.get(user=self.user, qry=que)
                uq.delete()

        permisos = self.data.getlist('u_permisos')

        for permiso in permisos:
            try:
                perm = Permission.objects.get(pk=permiso)
                self.user.user_permissions.add(perm)
            except Permission.DoesNotExist:
                pass

        user_permisos = [p.pk for p in self.user.user_permissions.all()]

        for permiso_usuario in user_permisos:
            if not str(permiso_usuario) in permisos:
                perm = Permission.objects.get(pk=permiso_usuario)
                self.user.user_permissions.remove(perm)

        profile = self.user.profile
        profile.efector_id = self.cleaned_data['efe_id']
        if self.cleaned_data['institucion_id']:
            profile.institucion_id = self.cleaned_data['institucion_id']
        profile.save()

        audit = AuditLog()
        audit.old_object = old_object
        audit.create_log_entry(self.user, action)

        return self.user


class UserAddForm(UserForm):
    def inserting(self):
        return True

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Ya existe un usuario con ese nombre de usuario')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')
        if not password1:
            raise forms.ValidationError('Debe ingresar una contraseña')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
