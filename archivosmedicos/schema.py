import graphql_jwt
import graphene

from graphene_django.debug import DjangoDebug
from django.conf import settings
from apps.persona import schema as personas_schema
from apps.profesionales import schema as profesional_schema


class Query(
    personas_schema.RelayQuery,
    profesional_schema.RelayQuery,
    graphene.ObjectType
):

    if settings.DEBUG:
        debug = graphene.Field(DjangoDebug, name='__debug')
    else:
        pass


class Mutation(
    personas_schema.RelayMutation,
    profesional_schema.RelayMutation,
    graphene.ObjectType
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
