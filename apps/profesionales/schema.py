import graphene
import django_filters

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.utils.html import escape

from apps.profesionales.models import (
    Profesional as ProfesionalModel,
    Especialidad as EspecialidadModel
)


def get_errors(e):
    fields = e.message_dict.keys()
    messages = ['; '.join(m) for m in e.message_dict.values()]
    errors = [i for pair in zip(fields, messages) for i in pair]
    return errors


class ProfesionalNode(DjangoObjectType):
    class Meta:
        model = ProfesionalModel
        interfaces = (graphene.relay.Node, )


class EspecialidadNode(DjangoObjectType):
    class Meta:
        model = EspecialidadModel
        interfaces = (graphene.relay.Node, )


class ProfesionalFilter(django_filters.FilterSet):
    nro_doc = django_filters.CharFilter(lookup_expr='icontains')
    apellido = django_filters.CharFilter(lookup_expr='icontains')
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    nro_matricula = django_filters.CharFilter(lookup_expr='icontains')
    especialidad = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ProfesionalModel
        fields = [
            'nro_doc',
            'fec_nac',
            'full_name',
            'apellido',
            'nombre',
            'nro_matricula',
            'especialidad'
        ]


class RelayQuery(graphene.ObjectType):
    relay_profesional = graphene.relay.Node.Field(ProfesionalNode)
    relay_profesional = DjangoFilterConnectionField(ProfesionalNode, filterset_class=ProfesionalFilter)


class RelayCreateProfesional(graphene.relay.ClientIDMutation):
    profesional = graphene.Field(ProfesionalNode)
    especialidad = graphene.Field(EspecialidadNode)

    class Input:
        apellido = graphene.String(required=True)
        nombre = graphene.String(required=True)
        nro_doc = graphene.String(required=True)
        doc_tipo = graphene.Int(required=True)
        sexo = graphene.Int(required=True)
        fec_nac = graphene.types.datetime.Date(required=True)
        tipo = graphene.Int(required=True)
        nro_matricula = graphene.String()
        especialidad = graphene.Int()
        clasificacion = graphene.Int()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        try:
            profesional = ProfesionalModel.objects.get(nro_matricula=input.get('nro_matricula'))
        except ProfesionalModel.DoesNotExist:
            profesional = ProfesionalModel(
                nro_matricula=escape(input.get('nro_matricula')),
                especialidad_id=input.get('especialidad'),
                clasificacion_id=input.get('clasificacion'),
                nombre=escape(input.get('nombre')),
                apellido=escape(input.get('apellido')),
                nro_doc=escape(input.get('nro_doc')),
                doc_tipo_id=input.get('doc_tipo'),
                sexo_id=input.get('sexo'),
                fec_nac=escape(input.get('fec_nac')),
                tipo_id=input.get('tipo')
            )
            profesional.save()
            return cls(profesional=profesional)
        return cls(profesional=None)


class RelayMutation(graphene.AbstractType):
    relay_create_profsional = RelayCreateProfesional.Field()
