from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Post:
    id: UUID
    content: PostContent


@dataclass(frozen=True)
class PostContent:
    weight: float
    size: float
