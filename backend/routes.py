import json
import graphene
from flask import send_from_directory, Response
from flask_graphql import GraphQLView
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from backend import models
from backend.application import backend_application
from backend.application.settings import BackendSettings
from backend.data_mining import DETAILED_COUNTRIES_API_LOOKUPS


class VirusDailyStatRecordObject(SQLAlchemyObjectType):
    class Meta:
        model = models.VirusDailyStatRecord
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    daily_update_records = SQLAlchemyConnectionField(VirusDailyStatRecordObject)


schema = graphene.Schema(query=Query)

backend_application.add_url_rule(
    "/graphql-api",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)


@backend_application.route("/detailed-countries", methods=["GET"])
def detailed_countries():
    return Response(
        json.dumps([country.casefold() for country in DETAILED_COUNTRIES_API_LOOKUPS])
    )


@backend_application.route("/<path:filename>", methods=["GET"])
def dev_frontend_test(filename):
    return send_from_directory(
        directory=f"{BackendSettings.BASE_DIR}/frontend", filename=filename
    )
