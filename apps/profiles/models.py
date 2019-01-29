# # Models
# # -*- coding: utf-8 -*-

# from django.db import models
# from django.contrib.auth.models import User
# from django.core.cache import cache

# from apps.profiles.cachekeys import key_profile_getprofile
# # from apps.efectores.models import Efector


# class Usuario(models.Model):
#     usr_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=20, null=False, db_column='usr_name')
#     pswd = models.CharField(max_length=100, null=False, db_column='usr_pswd')
#     nombre_completo = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'usuario'
#         verbose_name_plural = 'Usuarios'
#         permissions = (
#             ('manage_usuario', 'Can manage usuario'),
#         )

#     def __str__(self):
#         return self.name

#     @property
#     def user(self):
#         return self.userprofile.user

#     def get_full_name(self):
#         return self.user.get_full_name()

#     def get_pre_paquetes(self, flat=False):
#         if flat:
#             return list(self.pre_paquetes.values_list('paquete', flat=True))
#         else:
#             return self.pre_paquetes.all()

#     def get_pre_paquetes_choices(self):
#         result = []
#         for up in self.get_pre_paquetes():
#             result.append((up.paquete_id, up.paquete,))
#         return result


# # class UsuarioEfector(models.Model):
# #     usr_efe_id = models.AutoField(primary_key=True)
# #     usuario = models.ForeignKey(Usuario, db_column='usr_id', null=False, blank=False, related_name='efectores')
# #     efector = models.ForeignKey(Efector, db_column='efe_id', null=False, blank=False)

# #     class Meta:
# #         db_table = 'usuario_efector'
# #         unique_together = ('usuario', 'efector')
# #         verbose_name_plural = 'Usuarios Efectores'

# #     def __str__(self):
# #         return '%s-%s' % (self.usuario, self.efector,)


# # class UsuarioPrestacionPaquete(models.Model):
# #     usuario = models.ForeignKey(Usuario, null=False, blank=False, db_column='usr_id', related_name='pre_paquetes')
# #     paquete = models.ForeignKey('nomencladores.PrestacionPaquete', null=False, blank=False, db_column='pre_paq_id',
# #                                 related_name='usuario_paquetes')

# #     class Meta:
# #         db_table = 'usuario_paquete'
# #         verbose_name_plural = 'Asignacion a Usuarios de Paquetes'

# #     def __str__(self):
# #         return u'%s (%s)' % (self.usuario, self.paquete)

# #     @classmethod
# #     def get_paquetes(cls, usuario):
# #         return cls.objects.filter(usuario=usuario).order_by('paquete__pk')


# class UserProfile(models.Model):
#     """
#     Esta clase UserProfile representa el perfil del usuario web, es decir, el de
#     django User y relaciona el usuario del sistema con el usuario web
#     """
#     usr_profile_id = models.AutoField(primary_key=True)
#     user = models.OneToOneField(User, db_column='user_id', related_name='profile')
#     usuario = models.OneToOneField(Usuario, db_column='usr_id', null=True, blank=True)
#     efector = models.ForeignKey(Efector, db_column='efe_id', null=True, blank=True)
#     institucion = models.ForeignKey(Efector, db_column='efe_inst_id', null=True, blank=True, related_name='userprofile_inst')

#     class Meta:
#         db_table = 'usuario_profile'
#         unique_together = ('user', 'usuario')
#         verbose_name = 'Perfil de usuario'
#         verbose_name_plural = 'Usuarios Perfiles'

#     def __str__(self):
#         if self.usuario:
#             return '%s - %s' % (self.usuario.name, self.user.username)
#         return self.user.username

#     def save(self, *args, **kwargs):
#         self.clear_cache_key()
#         super(UserProfile, self).save(*args, **kwargs)

#     def clear_cache_key(self):
#         key = key_profile_getprofile(self.user)
#         cache.delete(key)

#     def is_related_efector(self, efe_id):
#         efe_id = int(efe_id)
#         if self.usuario.efectores.filter(efector_id=efe_id).exists():
#             return True
#         elif self.efector_id == efe_id:
#             return True
#         elif self.usuario.user.is_staff:
#             return True
#         else:
#             return False

#     def get_efector_count(self):
#         count = self.usuario.efectores.count()
#         if not count:
#             count = 1
#             # se considera que siempre hay un efector para cada UserProfile
#         return count

#     @property
#     def efectores(self):
#         return self.usuario.efectores.all()

#     @property
#     def pre_paquetes(self):
#         """Shortcut a los paquetes de prestaciones de usuarios"""
#         return self.usuario.pre_paquetes

#     def can_change_efector(self):
#         if self.user.is_staff:
#             return True
#         if self.usuario.efectores.count() > 0:
#             return True
#         return False


# def create_user_profile(sender, **kwargs):
#     if kwargs['created']:
#         user = kwargs['instance']
#         user_name = user.username[:20]
#         try:
#             usuario = Usuario.objects.get(name=user_name)
#         except Usuario.DoesNotExist:
#             usuario = Usuario()
#             usuario.name = user_name
#             usuario.pswd = user_name
#             usuario.nombre_completo = user.get_full_name()
#             usuario.save()

#         profile = UserProfile()
#         profile.user = user
#         profile.usuario = usuario
#         profile.save()

# models.signals.post_save.connect(create_user_profile, User)

