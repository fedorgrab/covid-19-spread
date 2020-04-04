import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from backend import models


class BookObject(SQLAlchemyObjectType):
    class Meta:
        model = models.VirusSpreadRecord
        interfaces = (graphene.relay.Node,)


# class UserObject(SQLAlchemyObjectType):
#     class Meta:
#         model = User
#         interfaces = (graphene.relay.Node,)
#
#
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_books = SQLAlchemyConnectionField(BookObject)


schema = graphene.Schema(query=Query)
