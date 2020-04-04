import graphene
from flask import send_from_directory
from flask_graphql import GraphQLView
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from backend import models
from backend.application import backend_application
from backend.application.settings import BackendSettings


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


@backend_application.route("/<path:filename>", methods=["GET"])
def dev_frontend_test(filename):
    return send_from_directory(
        directory=f"{BackendSettings.BASE_DIR}/frontend", filename=filename
    )
