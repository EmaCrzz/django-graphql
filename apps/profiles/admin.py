# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib import admin
from django.contrib.auth.models import User, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session
from django.contrib.contenttypes.models import ContentType

from . import models
from apps.qbuilder.models import QueryUser


class UserProfileInline(admin.TabularInline):
    model = models.UserProfile


class QueryUserInLine(admin.TabularInline):
    model = QueryUser
    extra = 0
    raw_id_fields = ('qry',)


class UserAdminEx(UserAdmin):
    actions = ['create_usuario']
    inlines = [UserProfileInline, QueryUserInLine]
    list_select_related = True
    list_per_page = 50
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'is_active', 'get_groups', 'get_usuario', 'get_efector',
        'last_login',
    )

    def has_profile(self, obj):
        return obj.profile is not None
    has_profile.short_description = 'Tiene profile'
    has_profile.boolean = True

    def has_usuario(self, obj):
        profile = obj.profile
        if profile:
            return profile.usuario is not None
        return False
    has_usuario.short_description = 'Tiene usuario interno'
    has_usuario.boolean = True

    def get_groups(self, obj):
        if obj.is_superuser:
            return '[SUPER USUARIO]'

        s = ''
        p = ''
        for grp in obj.groups.all():
            s += p + grp.name
            p = ' / '
        return s
    get_groups.short_description = 'Grupos'

    def get_usuario(self, obj):
        profile = obj.profile
        if not profile:
            return "(Sin Profile)"
        if profile.usuario:
            return '%s (%s)' % (profile.usuario, profile.usuario.pk)
        return None
    get_usuario.short_description = 'Usuario interno'

    def get_efector(self, obj):
        profile = obj.profile
        if not profile:
            return None
        if profile.efector_id:
            e = models.Efector.objects.values('efe_nombre').get(pk=profile.efector_id)
            return '%(efe_nombre)s' % e
        return None
    get_efector.short_description = 'Efector'

    def create_profile(self, request, queryset):
        pass

    def delete_profile(self, request, queryset):
        pass


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'codename',)
    search_fields = ('name',)
    list_filter = ('content_type',)


class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'expire_date', 'get_user',)
    search_fields = ('session_key',)
    readonly_fields = ('session_key', 'session_data', 'expire_date',)
    actions = ['cleanup_sessions']

    def queryset(self, request):
        qs = super(SessionAdmin, self).queryset(request)
        return qs.filter(expire_date__gte=datetime.now())

    def get_user(self, obj):
        result = ''
        data = obj.get_decoded()
        uid = data.get('_auth_user_id', None)
        if uid:
            user = User.objects.get(pk=uid)
            efe = user.profile.efector
            result = '%s  [ %s ]' % (user, efe or 'S/D')
        return result
    get_user.short_description = 'Usuario'

    def cleanup_sessions(self, request, queryset):
        for s in queryset.filter(expire_date__lt=datetime.now()).all():
            s.delete()
    cleanup_sessions.short_description = 'Eliminar sesiones que expiraron'


class UsuarioEfectorInline(admin.TabularInline):
    model = models.UsuarioEfector


# class UsuarioPrestacionPaquete(admin.TabularInline):
#     model = models.UsuarioPrestacionPaquete


class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'get_user', 'get_efector', 'get_user_is_staff',
        'get_last_login',
    )
    list_select_related = True
    list_per_page = 50
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [UsuarioEfectorInline, UserProfileInline]

    def _has_user_web(self, obj):
        return (obj.userprofile and obj.userprofile.user)

    def get_user(self, obj):
        if obj.userprofile:
            return obj.userprofile.user
        return None
    get_user.short_description = 'User web'

    def get_user_is_staff(self, obj):
        if self._has_user_web(obj):
            return obj.userprofile.user.is_staff
        return False
    get_user_is_staff.short_description = 'Staff'
    get_user_is_staff.boolean = True

    def get_last_login(self, obj):
        if self._has_user_web(obj):
            return obj.userprofile.user.last_login
    get_last_login.short_description = 'Último ingreso'

    def get_efector(self, obj):
        if obj.userprofile:
            return obj.userprofile.efector
        return None
    get_efector.short_description = 'Efector'


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'get_full_name', 'usuario', 'efector',
        'get_user_is_staff',
    )
    list_filter = ('efector',)

    def get_full_name(self, obj):
        return '%s %s' % (obj.user.last_name, obj.user.first_name)
    get_full_name.short_description = 'Apellido y Nombre'

    def get_user_is_staff(self, obj):
        return obj.user.is_staff
    get_user_is_staff.short_description = 'Is Staff'
    get_user_is_staff.boolean = True


# -----------------------------------------------------------------------------
admin.site.unregister(User)
admin.site.register(User, UserAdminEx)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(ContentType)
admin.site.register(models.Usuario, UsuarioAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.UsuarioEfector)
# admin.site.register(models.UsuarioPrestacionPaquete)
