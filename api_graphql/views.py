from braces import views

from graphene_django.views import GraphQLView


class SuperUserGraphQLView(
    views.LoginRequiredMixin,
    views.SuperuserRequiredMixin,
    GraphQLView
):
    pass
