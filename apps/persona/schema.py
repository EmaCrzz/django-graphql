import graphene
import django_filters

from django.core.exceptions import ValidationError
from django.utils.html import escape
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from apps.persona.models import (
    Persona as PersonaModel,
    PersonaTipo as PersonaTipoModel,
    PerDom as PerDomModel,
    PerTel as PerTelModel,
    PerEmail as PerEmailModel
)
from apps.core.models import (
    Sexo as SexoModel,
    Localidad as LocalidadModel,
    Municipio as MunicipioModel,
    TelClasif as TelClasifModel,
    TelTipo as TelTipoModel,
    EmailClasif as EmailClasifModel
)

from apps.core.schema import (
    LocalidadNode,
    MunicipioNode,
    SexoNode,
    TelTipoNode,
    TelClasifNode,
    EmailClasifNode
)


def get_errors(e):
    fields = e.message_dict.keys()
    messages = ['; '.join(m) for m in e.message_dict.values()]
    errors = [i for pair in zip(fields, messages) for i in pair]
    return errors


class PersonaNode(DjangoObjectType):
    class Meta:
        model = PersonaModel
        interfaces = (graphene.relay.Node, )


class PersonaTipoNode(DjangoObjectType):
    class Meta:
        model = PersonaTipoModel
        interfaces = (graphene.relay.Node,)


class PerDomNode(DjangoObjectType):
    class Meta:
        model = PerDomModel
        interfaces = (graphene.relay.Node, )


class PerTelNode(DjangoObjectType):
    class Meta:
        model = PerTelModel
        interfaces = (graphene.relay.Node, )


class PerEmailNode(DjangoObjectType):
    class Meta:
        model = PerEmailModel
        interfaces = (graphene.relay.Node, )


class PersonaFilter(django_filters.FilterSet):
    nro_doc = django_filters.CharFilter(lookup_expr='icontains')
    apellido = django_filters.CharFilter(lookup_expr='icontains')
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = PersonaModel
        fields = [
            'nro_doc',
            'fec_nac',
            'full_name',
            'apellido',
            'nombre'
        ]


class PersonaTipoFilter(django_filters.FilterSet):
    class Meta:
        model = PersonaTipoModel
        fields = ['per_tipo_id', 'descripcion']


class RelayQuery(graphene.ObjectType):
    relay_persona = graphene.relay.Node.Field(PersonaNode)
    relay_persona = DjangoFilterConnectionField(PersonaNode, filterset_class=PersonaFilter)
    relay_persona_tipo = graphene.relay.Node.Field(PersonaTipoNode)
    relay_persona_tipo = DjangoFilterConnectionField(PersonaTipoNode, filterset_class=PersonaTipoFilter)


# Mutaciones
#  insert


class RelayCreatePersona(graphene.relay.ClientIDMutation):
    persona = graphene.Field(PersonaNode)
    persona_tipo = graphene.Field(PersonaTipoNode)
    sexo = graphene.Field(SexoNode)

    # datos de entrada
    class Input:
        apellido = graphene.String(required=True)
        nombre = graphene.String(required=True)
        nro_doc = graphene.String(required=True)
        doc_tipo = graphene.Int(required=True)
        sexo = graphene.Int(required=True)
        fec_nac = graphene.types.datetime.Date(required=True)
        tipo = graphene.Int(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # guardo la instancia de tipo de persona filtrado por el campo id
        persona_tipo = PersonaTipoModel.objects.filter(
            per_tipo_id=input.get('tipo')
        )

        if not persona_tipo:
            raise Exception('Invalid Tipo Persona')

        # guardo el sexo filtrado por el campo id
        sexo_tipo = SexoModel.objects.filter(
            sexo_id=input.get('sexo')
        )

        if not sexo_tipo:
            raise Exception('Invalid Sexo')

        try:
            persona = PersonaModel.objects.get(nro_doc=input.get('nro_doc'))
        except PersonaModel.DoesNotExist:
            # creo la instancia proveedor y guardo los datos
            persona = PersonaModel(
                nombre=escape(input.get('nombre')),
                apellido=escape(input.get('apellido')),
                nro_doc=escape(input.get('nro_doc')),
                doc_tipo_id=input.get('doc_tipo'),
                sexo_id=input.get('sexo'),
                fec_nac=escape(input.get('fec_nac')),
                tipo_id=input.get('tipo')

            )
            persona.save()
            return cls(persona=persona)
        return cls(persona=None)


class RelayUpdatePersona(graphene.relay.ClientIDMutation):
    persona = graphene.Field(PersonaNode)
    persona_tipo = graphene.Field(PersonaTipoNode)

    class Input:
        nombre = graphene.String(required=True)
        apellido = graphene.String(required=True)
        nro_doc = graphene.String(required=True)
        per_tipo_id = graphene.Int(required=True)
        id = graphene.String(required=True)

    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        persona_tipo = PersonaTipoModel.objects.get(
            per_tipo_id=input.get('per_tipo_id')
        )
        if not persona_tipo:
            raise Exception('Invalid Tipo Persona')

        try:
            persona = PersonaModel.objects.get(pk=input.get('id'))
            if persona:
                # modificar y actualizar la instancia del modelo persona
                if persona.nro_doc != input.get('nro_doc'):
                    persona_nro_doc = PersonaModel.objects.filter(
                        nro_doc=input.get('nro_doc')
                    ).exclude(nro_doc=persona.nro_doc)
                    if persona_nro_doc:
                        return cls(proveedor=None)
                    else:
                        persona.nro_doc = escape(input.get('nro_doc'))
                else:
                    persona.nro_doc = escape(input.get('nro_doc'))

                persona.nombre = escape(input.get('nombre'))
                persona.apellido = escape(input.get('apellido'))
                persona.tipo_id = persona_tipo.per_tipo_id
                persona.save()

                return cls(persona=persona)

        except ValidationError as e:
            # retorna el mensaje del error
            return cls(persona=None, errors=get_errors(e))


class RelayDeletePersona(graphene.relay.ClientIDMutation):
    persona = graphene.Field(PersonaNode)
    persona_tipo = graphene.Field(PersonaTipoNode)

    class Input:
        id = graphene.String(required=True)

    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        try:
            persona = PersonaModel.objects.filter(per_id=input.get('id'))
            if persona:
                persona.delete()
                return cls(persona=persona)
        except PersonaModel.DoesNotExist as e:
            # retorna el mensaje del error
            return cls(persona=None, errors=get_errors(e))


class RelayCreatePerDom(graphene.relay.ClientIDMutation):
    per_dom = graphene.Field(PerDomNode)
    localidad = graphene.Field(LocalidadNode)
    municipio = graphene.Field(MunicipioNode)

    class Input:
        persona = graphene.Int(required=True)
        calle = graphene.String(required=True)
        nro_puerta = graphene.String(required=True)
        piso = graphene.String(required=False)
        dpto = graphene.String(required=False)
        mzna = graphene.String(required=False)
        lote = graphene.String(required=False)
        entre_calle = graphene.String(required=False)
        y_calle = graphene.String(required=False)
        cpa = graphene.String(required=False)
        localidad = graphene.Int(required=True)
        municipio = graphene.Int(required=False)
        barrio = graphene.String(required=False)
        observaciones = graphene.String(required=False)
        predeterminado = graphene.Boolean()

    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        persona = PersonaModel.objects.get(
            pk=input.get('persona')
        )
        if not persona:
            raise Exception('Invalid Persona')

        localidad = LocalidadModel.objects.get(pk=input.get('localidad'))
        if not localidad:
            raise Exception('Invalid Localidad')
        municipio = MunicipioModel.objects.get(pk=input.get('municipio'))
        if not municipio:
            raise Exception('Invalid Municipio')
        # creo la instancia perdom y guardo los datos
        per_dom = PerDomModel(
            persona=persona,
            calle=escape(input.get('calle')),
            nro_puerta=escape(input.get('nro_puerta')),
            piso=escape(input.get('piso')),
            dpto=escape(input.get('dpto')),
            mzna=escape(input.get('mzna')),
            lote=escape(input.get('lote')),
            entre_calle=escape(input.get('entre_calle')),
            y_calle=escape(input.get('y_calle')),
            cpa=escape(input.get('cpa')),
            localidad=localidad,
            municipio=municipio,
            barrio=escape(input.get('barrio')),
            observaciones=escape(input.get('observaciones')),
            predeterminado=input.get('predeterminado')
        )
        per_dom.save()
        return cls(per_dom=per_dom)


class RelayUpdatePerDom(graphene.relay.ClientIDMutation):
    per_dom = graphene.Field(PerDomNode)
    localidad = graphene.Field(LocalidadNode)
    municipio = graphene.Field(MunicipioNode)

    class Input:
        persona = graphene.Int(required=True)
        calle = graphene.String(required=True)
        nro_puerta = graphene.String(required=True)
        piso = graphene.String(required=False)
        dpto = graphene.String(required=False)
        mzna = graphene.String(required=False)
        lote = graphene.String(required=False)
        entre_calle = graphene.String(required=False)
        y_calle = graphene.String(required=False)
        cpa = graphene.String(required=False)
        localidad = graphene.Int(required=True)
        municipio = graphene.Int(required=False)
        barrio = graphene.String(required=False)
        observaciones = graphene.String(required=False)
        predeterminado = graphene.Boolean()
        id = graphene.Int(required=True)

    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        persona = PersonaModel.objects.get(
            pk=input.get('persona')
        )
        if not persona:
            raise Exception('Invalid Persona')

        localidad = LocalidadModel.objects.get(pk=input.get('localidad'))
        if not localidad:
            raise Exception('Invalid Localidad')
        municipio = MunicipioModel.objects.get(pk=input.get('municipio'))
        if not municipio:
            raise Exception('Invalid Municipio')

        try:
            per_dom = PerDomModel.objects.get(pk=input.get('id'))
            if per_dom:
                per_dom.calle = escape(input.get('calle'))
                per_dom.nro_puerta = escape(input.get('nro_puerta'))
                per_dom.piso = escape(input.get('piso'))
                per_dom.dpto = escape(input.get('dpto'))
                per_dom.mzna = escape(input.get('mzna'))
                per_dom.lote = escape(input.get('lote'))
                per_dom.entre_calle = escape(input.get('entre_calle'))
                per_dom.y_calle = escape(input.get('y_calle'))
                per_dom.cpa = escape(input.get('cpa'))
                per_dom.localidad = localidad
                per_dom.municipio = municipio
                per_dom.barrio = escape(input.get('barrio'))
                per_dom.observaciones = escape(input.get('observaciones'))
                per_dom.predeterminado = input.get('predeterminado')
                per_dom.save()
            return cls(per_dom=per_dom)

        except ValidationError as e:
            # retorna el mensaje del error
            return cls(per_dom=None, errors=get_errors(e))


class RelayDeletePerDom(graphene.relay.ClientIDMutation):
    per_dom = graphene.Field(PerDomNode)

    class Input:
        id = graphene.Int(required=True)

    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        try:
            per_dom = PerDomModel.objects.filter(pk=input.get('id'))
            if per_dom:
                per_dom.delete()
                return cls(per_dom=per_dom)
        except PerDomModel.DoesNotExist as e:
            # retorna el mensaje del error
            return cls(per_dom=None, errors=get_errors(e))


class RelayCreatePerTel(graphene.relay.ClientIDMutation):
    per_tel = graphene.Field(PerTelNode)
    per_tipo = graphene.Field(TelTipoNode)
    per_clasif = graphene.Field(TelClasifNode)

    class Input:
        persona = graphene.Int(required=True)
        tel_clasif = graphene.Int(required=True)
        tel_tipo = graphene.Int(required=True)
        cod_pais = graphene.String(required=False)
        cod_area = graphene.String(required=True)
        nro_tel = graphene.String(required=True)
        observaciones = graphene.String(required=False)
        predeterminado = graphene.Boolean(default=False)

    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        persona = PersonaModel.objects.get(
            pk=input.get('persona')
        )
        if not persona:
            raise Exception('Invalid Persona')

        tel_clasif = TelClasifModel.objects.get(pk=input.get('tel_clasif'))
        if not tel_clasif:
            raise Exception('Invalid Tel Clasif.')

        tel_tipo = TelTipoModel.objects.get(pk=input.get('tel_tipo'))
        if not tel_tipo:
            raise Exception('Invalid Tel Tipo')

        per_tel = PerTelModel(
            persona=persona,
            tel_clasif=tel_clasif,
            tel_tipo=tel_tipo,
            cod_pais=escape(input.get('cod_pais')),
            cod_area=escape(input.get('cod_area')),
            nro_tel=escape(input.get('nro_tel')),
            observaciones=escape(input.get('observaciones')),
            predeterminado=escape(input.get('predeterminado'))
        )
        per_tel.save()
        return cls(per_tel=per_tel)


class RelayUpdatePerTel(graphene.relay.ClientIDMutation):
    per_tel = graphene.Field(PerTelNode)
    per_tipo = graphene.Field(TelTipoNode)
    per_clasif = graphene.Field(TelClasifNode)

    class Input:
        id = graphene.Int(required=True)
        persona = graphene.Int(required=True)
        tel_clasif = graphene.Int(required=True)
        tel_tipo = graphene.Int(required=True)
        cod_pais = graphene.String(required=False)
        cod_area = graphene.String(required=True)
        nro_tel = graphene.String(required=True)
        observaciones = graphene.String(required=False)
        predeterminado = graphene.Boolean(default=False)

    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        persona = PersonaModel.objects.get(
            pk=input.get('persona')
        )
        if not persona:
            raise Exception('Invalid Persona')

        tel_clasif = TelClasifModel.objects.get(pk=input.get('tel_clasif'))
        if not tel_clasif:
            raise Exception('Invalid Tel Clasif.')

        tel_tipo = TelTipoModel.objects.get(pk=input.get('tel_tipo'))
        if not tel_tipo:
            raise Exception('Invalid Tel Tipo')

        try:
            per_tel = PerTelModel.objects.get(pk=input.get('id'))
            if per_tel:
                per_tel.tel_clasif = tel_clasif
                per_tel.tel_tipo = tel_tipo
                per_tel.cod_pais = escape(input.get('cod_pais'))
                per_tel.cod_area = escape(input.get('cod_area'))
                per_tel.nro_tel = escape(input.get('nro_tel'))
                per_tel.observaciones = escape(input.get('observaciones'))
                per_tel.predeterminado = escape(input.get('predeterminado'))
                per_tel.save()
            return cls(per_tel=per_tel)

        except ValidationError as e:
            # retorna el mensaje del error
            return cls(per_tel=None, errors=get_errors(e))


class RelayDeletePerTel(graphene.relay.ClientIDMutation):
    per_tel = graphene.Field(PerTelNode)

    class Input:
        id = graphene.Int(required=True)

    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        try:
            per_tel = PerTelModel.objects.filter(pk=input.get('id'))
            if per_tel:
                per_tel.delete()
                return cls(per_tel=per_tel)
        except PerTelModel.DoesNotExist as e:
            # retorna el mensaje del error
            return cls(per_tel=None, errors=get_errors(e))


class RelayCreatePerEmail(graphene.relay.ClientIDMutation):
    per_email = graphene.Field(PerEmailNode)
    email_clasif = graphene.Field(EmailClasifNode)

    class Input:
        persona = graphene.Int(required=True)
        email_clasif = graphene.Int(required=True)
        email = graphene.String(required=True)
        observaciones = graphene.String(required=False)
        predeterminado = graphene.Boolean(default=False)

    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        persona = PersonaModel.objects.get(
            pk=input.get('persona')
        )
        if not persona:
            raise Exception('Invalid Persona')

        email_clasif = EmailClasifModel.objects.get(pk=input.get('email_clasif'))
        if not email_clasif:
            raise Exception('Invalid Email Clasif')

        per_email = PerEmailModel(
            persona=persona,
            email_clasif=email_clasif,
            email=escape(input.get('email')),
            observaciones=escape(input.get('observaciones')),
            predeterminado=escape(input.get('predeterminado'))
        )
        per_email.save()
        return cls(per_email=per_email)


class RelayUpdatePerEmail(graphene.relay.ClientIDMutation):
    per_email = graphene.Field(PerEmailNode)
    email_clasif = graphene.Field(EmailClasifNode)

    class Input:
        persona = graphene.Int(required=True)
        id = graphene.Int(required=True)
        email_clasif = graphene.Int(required=True)
        email = graphene.String(required=True)
        observaciones = graphene.String(required=False)
        predeterminado = graphene.Boolean(default=False)

    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        persona = PersonaModel.objects.get(
            pk=input.get('persona')
        )
        if not persona:
            raise Exception('Invalid Persona')

        email_clasif = EmailClasifModel.objects.get(pk=input.get('email_clasif'))

        if not email_clasif:
            raise Exception('Invalid Email Clasif')

        try:
            per_email = PerEmailModel.objects.get(pk=input.get('id'))
            if per_email:
                per_email.email_clasif = email_clasif
                per_email.email = escape(input.get('email'))
                per_email.observaciones = escape(input.get('observaciones'))
                per_email.predeterminado = escape(input.get('predeterminado'))
                per_email.save()
            return cls(per_email=per_email)

        except ValidationError as e:
            # retorna el mensaje del error
            return cls(per_email=None, errors=get_errors(e))


class RelayDeletePerEmail(graphene.relay.ClientIDMutation):
    per_email = graphene.Field(PerEmailNode)

    class Input:
        id = graphene.Int(required=True)

    errors = graphene.List(graphene.String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        try:
            per_email = PerEmailModel.objects.get(pk=input.get('id'))
            if per_email:
                per_email.delete()
                return cls(per_email=per_email)
        except PerEmailModel.DoesNotExist as e:
            # retorna el mensaje del error
            return cls(per_email=None, errors=get_errors(e))


class RelayMutation(graphene.AbstractType):
    relay_create_persona = RelayCreatePersona.Field()
    relay_update_persona = RelayUpdatePersona.Field()
    relay_delete_persona = RelayDeletePersona.Field()
    relay_create_per_dom = RelayCreatePerDom.Field()
    relay_update_per_dom = RelayUpdatePerDom.Field()
    relay_delete_per_dom = RelayDeletePerDom.Field()
    relay_create_per_tel = RelayCreatePerTel.Field()
    relay_update_per_tel = RelayUpdatePerTel.Field()
    relay_delete_per_tel = RelayDeletePerTel.Field()
    relay_create_per_email = RelayCreatePerEmail.Field()
    relay_update_per_email = RelayUpdatePerEmail.Field()
    relay_delete_per_email = RelayDeletePerEmail.Field()
