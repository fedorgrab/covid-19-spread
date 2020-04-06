import json
import graphene
from flask import send_from_directory, Response
from flask_graphql import GraphQLView
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from backend import models
from backend.application import backend_application
from backend.application.settings import BackendSettings
from backend.data_mining import DETAILED_COUNTRIES


class VirusDailyStatRecordObject(SQLAlchemyObjectType):
    class Meta:
        model = models.VirusDailyStatRecord
        interfaces = (graphene.relay.Node,)


class VirusDayOneRecord(SQLAlchemyObjectType):
    class Meta:
        model = models.VirusDayOneByCountry
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            # 'pk': ['exact'],
            # 'detail': ['icontains', 'istartswith'],
            # 'created_by__name': ['icontains', ],
            # 'hidden': ['exact'],
            # 'report': ['exact'],
            "country": ["exact"]
        }


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    daily_update_records = SQLAlchemyConnectionField(VirusDailyStatRecordObject)

    day_one_records = SQLAlchemyConnectionField(VirusDayOneRecord, country=graphene.String())

    def resolve_day_one_records(self, info, country):
        country = "".join([country[0].capitalize(), country[1:]])
        return models.VirusDayOneByCountry.query.filter_by(country=country)


schema = graphene.Schema(query=Query)

backend_application.add_url_rule(
    "/graphql-api",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)


@backend_application.route("/detailed-countries", methods=["GET"])
def detailed_countries():
    return Response(
        json.dumps([country.casefold() for country in DETAILED_COUNTRIES])
    )


@backend_application.route("/<path:filename>", methods=["GET"])
def dev_frontend_test(filename):
    return send_from_directory(
        directory=f"{BackendSettings.BASE_DIR}/frontend", filename=filename
    )
