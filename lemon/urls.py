from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from lemon.schema.schema import schema

urlpatterns = [
    path('graphql', csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=True)))
]