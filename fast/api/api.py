from uuid import UUID

from graphene import (ObjectType, Schema, Float, ID, Field, List, NonNull, Argument,
                      InputObjectType, Mutation, Boolean)

from fast.api import entity
from fast.api.repository import Repository


def get_api_schema(repository: Repository) -> Schema:
    class Post(ObjectType):
        uuid = ID()
        weight = Float()
        size = Float()

    class PostFilterInput(InputObjectType):
        uuid = ID()

    class DeletePost(Mutation):
        class Arguments:
            uuid = ID(required=True)

        ok = Boolean()

        def mutate(root, info, uuid):
            repository.delete(UUID(uuid))
            return DeletePost()

    class UpsertPost(Mutation):
        class Arguments:
            uuid = ID(required=False)
            weight = Float(required=True)
            size = Float(required=True)

        post = Field(lambda: Post, required=True)

        def mutate(root, info, weight, size, uuid=None):
            if uuid is None:
                uuid = repository.create(entity.PostContent(
                    weight=weight,
                    size=size,
                ))
            else:
                repository.update(UUID(uuid), entity.PostContent(
                    weight=weight,
                    size=size,
                ))
            return UpsertPost(post=Post(
                uuid=uuid,
                weight=weight,
                size=size,
            ))

    class Mutations(ObjectType):
        upsert_post = UpsertPost.Field()
        delete_post = DeletePost.Field()

    class Query(ObjectType):
        posts = Field(
            List(NonNull(Post)),
            post_filter=Argument(PostFilterInput, required=True))

        def resolve_posts(parent, info, post_filter: PostFilterInput):
            if post_filter.uuid is None:
                return [Post(
                    uuid=p.id,
                    weight=p.content.weight,
                    size=p.content.size,
                ) for p in repository.list()]
            else:
                p = repository.get(UUID(post_filter.uuid))
                if not p:
                    return []
                return [Post(
                    uuid=p.id,
                    weight=p.content.weight,
                    size=p.content.size,
                )]

    return Schema(query=Query, mutation=Mutations)
