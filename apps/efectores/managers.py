# -*- coding: utf-8 -*-

from django.db import models


class EfectorManager(models.Manager):
    def get_queryset(self):
        return super(EfectorManager, self).get_queryset().filter(integrante=True)
