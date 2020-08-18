import uuid
from typing import Optional, List

from pymongo import MongoClient

from fast.api import entity
from fast.api.entity import Post, PostContent


def post_to_database(p: Post) -> dict:
    return {
        'uuid': str(p.id),
        'content': {
            'weight': p.content.weight,
            'size': p.content.size,
        }
    }


def post_from_database(p: dict) -> Post:
    return Post(
        id=p['uuid'],
        content=PostContent(
            weight=p['content']['weight'],
            size=p['content']['size'],
        ),
    )


class Repository:
    def __init__(self, mongo_client: MongoClient):
        self.post_collection = mongo_client.fast.post
        self.post_collection.create_index("uuid")

    def create(self, post_content: entity.PostContent) -> uuid.UUID:
        post = Post(
            id=uuid.uuid4(),
            content=post_content,
        )
        self.post_collection.insert_one(post_to_database(post))
        return post.id

    def update(self, id: uuid.UUID, post_content: entity.PostContent) -> None:
        post = Post(
            id=id,
            content=post_content,
        )
        self.post_collection.update_one({'uuid': str(id)}, {
            "$set": post_to_database(post),
        })

    def get(self, id: uuid.UUID) -> Optional[Post]:
        result = self.post_collection.find_one({"uuid": str(id)})
        if result is None:
            return None

        return post_from_database(result)

    def list(self) -> List[Post]:
        result = (post for post in self.post_collection.find())
        result = (post_from_database(post) for post in result)
        return list(result)

    def delete(self, id: uuid.UUID) -> None:
        self.post_collection.delete_one({'uuid': str(id)})
