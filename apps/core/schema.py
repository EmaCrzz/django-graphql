import graphene

from graphene_django import DjangoObjectType

from apps.core.models import (
    Sexo as SexoModel,
    Localidad as LocalidadModel,
    Municipio as MunicipioModel,
    TelClasif as TelClasifModel,
    TelTipo as TelTipoModel,
    EmailClasif as EmailClasifModel
)


class LocalidadNode(DjangoObjectType):
    class Meta:
        model = LocalidadModel
        interfaces = (graphene.relay.Node, )


class MunicipioNode(DjangoObjectType):
    class Meta:
        model = MunicipioModel
        interfaces = (graphene.relay.Node, )


class SexoNode(DjangoObjectType):
    class Meta:
        model = SexoModel
        interfaces = (graphene.relay.Node, )


class TelClasifNode(DjangoObjectType):
    class Meta:
        model = TelClasifModel
        interfaces = (graphene.relay.Node, )


class TelTipoNode(DjangoObjectType):
    class Meta:
        model = TelTipoModel
        interfaces = (graphene.relay.Node, )


class EmailClasifNode(DjangoObjectType):
    class Meta:
        model = EmailClasifModel
        interfaces = (graphene.relay.Node, )
