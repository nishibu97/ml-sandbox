import strawberry

from app.features.users.repository import list_users


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str


@strawberry.type
class Query:
    @strawberry.field
    async def users(self) -> list[User]:
        return [User(**row) for row in list_users()]


schema = strawberry.Schema(Query)