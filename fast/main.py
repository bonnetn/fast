from __future__ import annotations

from flask import Flask
from flask_graphql import GraphQLView
from pymongo import MongoClient

from fast.api.api import get_api_schema
from fast.api.repository import Repository

app = Flask(__name__)

if __name__ == '__main__':
    client = MongoClient(username='root', password='root')
    repository = Repository(client)
    schema = get_api_schema(repository)

    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    ))

    app.run()
