from django.contrib import admin
from django.urls import path
from .views import about
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from company_pages.schema import schema


urlpatterns = [
    path(
        "graphql",
        csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)),
        name="vehicle-graphql",
    ),
]
