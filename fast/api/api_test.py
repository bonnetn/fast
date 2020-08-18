import uuid
from unittest.mock import MagicMock

import pytest

from fast.api import entity
from fast.api.api import get_api_schema


@pytest.fixture
def repository():
    return MagicMock()


@pytest.fixture
def schema(repository):
    return get_api_schema(repository)


def test_list(repository, schema):
    repository.list = MagicMock(return_value=[
        entity.Post(
            id=uuid.UUID('11111111-1111-1111-1111-111111111111'),
            content=entity.PostContent(
                weight=1,
                size=2,
            )
        )

    ])
    result = schema.execute('''
    query Query {
        posts(postFilter: {}) {
            uuid
            weight
            size
        }
    }
    ''')
    assert result.data == {
        'posts': [{
            'uuid': '11111111-1111-1111-1111-111111111111',
            'weight': 1.,
            'size': 2.,
        }]
    }


def test_get(repository, schema):
    repository.get = MagicMock(return_value=entity.Post(
        id=uuid.UUID('11111111-1111-1111-1111-111111111111'),
        content=entity.PostContent(
            weight=1,
            size=2,
        )
    ))
    result = schema.execute('''
    query Query {
        posts(postFilter: {uuid:"11111111-1111-1111-1111-111111111111"}) {
            uuid
            weight
            size
        }
    }
    ''')
    assert result.data == {
        'posts': [{
            'uuid': '11111111-1111-1111-1111-111111111111',
            'weight': 1.,
            'size': 2.,
        }]
    }
    repository.get.assert_called_once_with(uuid.UUID('11111111-1111-1111-1111-111111111111'))


def test_delete(repository, schema):
    repository.delete = MagicMock(return_value=None)
    schema.execute('''
    mutation Mutations {
        deletePost(uuid: "11111111-1111-1111-1111-111111111111") {
            ok
        }
    }
    ''')
    repository.delete.assert_called_once_with(uuid.UUID('11111111-1111-1111-1111-111111111111'))


def test_update(repository, schema):
    repository.update = MagicMock(return_value=None)
    result = schema.execute('''
    mutation Mutations {
        upsertPost(uuid: "11111111-1111-1111-1111-111111111111", size: 1, weight: 2) {
            post {
                uuid
                weight
                size
            }
        }
    }
    ''')
    assert result.data == {
        'upsertPost': {
            'post': {
                'uuid': '11111111-1111-1111-1111-111111111111',
                'weight': 2.,
                'size': 1.,
            }
        }
    }
    repository.update.assert_called_once_with(uuid.UUID('11111111-1111-1111-1111-111111111111'),
                                              entity.PostContent(weight=2., size=1.))


def test_create(repository, schema):
    repository.create = MagicMock(return_value=uuid.UUID('11111111-1111-1111-1111-111111111111'))
    result = schema.execute('''
    mutation Mutations {
        upsertPost(size: 1, weight: 2) {
            post {
                uuid
                weight
                size
            }
        }
    }
    ''')
    assert result.data == {
        'upsertPost': {
            'post': {
                'uuid': '11111111-1111-1111-1111-111111111111',
                'weight': 2.,
                'size': 1.,
            }
        }
    }
    repository.create.assert_called_once_with(entity.PostContent(weight=2., size=1.))
