from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Optional
from uuid import UUID

from jsonschema import validate, ValidationError


@dataclass
class Post:
    id: UUID
    content: PostContent

    @staticmethod
    def to_api(post: Post) -> dict:
        return {
            'id': post.id,
            **PostContent.to_api(post.content),
        }

    @staticmethod
    def from_database(mongo_document: dict) -> Post:
        return Post(
            id=mongo_document['uuid'],
            content=PostContent.from_database(mongo_document['content'])
        )

    @staticmethod
    def to_database(p: Post) -> dict:
        return {
            'uuid': str(p.id),
            'content': PostContent.to_database(p.content),
        }


@dataclass
class PostContent:
    weight: float
    size: float

    @staticmethod
    def from_api(api_payload: dict) -> Tuple[Optional[PostContent], str]:
        try:
            validate(instance=api_payload, schema={
                "type": "object",
                "properties": {
                    "weight": {"type": "number"},
                    "size": {"type": "number"},
                },
                "required": ["weight", "size"]
            })
        except ValidationError as e:
            return None, e.message

        return PostContent(
            weight=api_payload['weight'],
            size=api_payload['size'],
        ), ''

    @staticmethod
    def to_api(post_content: PostContent) -> dict:
        return {
            'weight': post_content.weight,
            'size': post_content.size,
        }

    @staticmethod
    def from_database(mongo_document: dict) -> PostContent:
        return PostContent(
            weight=mongo_document['weight'],
            size=mongo_document['size'],
        )

    @staticmethod
    def to_database(post_content: PostContent) -> dict:
        return {
            'weight': post_content.weight,
            'size': post_content.size,
        }
