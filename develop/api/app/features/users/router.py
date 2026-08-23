from strawberry.fastapi import GraphQLRouter

from app.features.users.schema import schema

router = GraphQLRouter(schema)