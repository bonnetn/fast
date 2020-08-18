from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4

from flask import Response, jsonify, Flask, request, make_response
from flask.views import MethodView, View
from pymongo import MongoClient

from fast.entity import Post, PostContent

app = Flask(__name__)


def to_uuid(s: str) -> Optional[UUID]:
    try:
        return UUID(s)
    except ValueError:
        return None


def create_post_api_view(mongo_client: MongoClient) -> View:
    post_collection = mongo_client.fast.post
    post_collection.create_index("uuid")

    class PostAPI(MethodView):
        def get(self, post_id: Optional[str]) -> Response:
            if post_id is not None:
                return self._get_by_id(post_id)
            else:
                return self._list()

        def _get_by_id(self, post_id: str) -> Response:
            uuid = to_uuid(post_id)
            if uuid is None:
                return Response(f'invalid uuid {post_id}', status=400)

            result = post_collection.find_one({"uuid": str(uuid)})
            if result is None:
                return Response(f'no post {uuid} found', status=404)

            post_content = Post.to_api(Post.from_database(result))
            return jsonify(post_content)

        def _list(self) -> Response:
            result = (post for post in post_collection.find())
            result = (Post.from_database(post) for post in result)
            result = (post.to_api(post) for post in result)
            return jsonify(list(result))

        def post(self):
            json_payload = request.get_json()
            if json_payload is None:
                return Response('no json payload', status=400)

            content, failure_reason = PostContent.from_api(json_payload)
            if content is None:
                return Response(failure_reason, status=400)

            post = Post(
                id=uuid4(),
                content=content,
            )

            post_collection.insert_one(Post.to_database(post))
            return make_response(jsonify({
                "uuid": str(post.id),
            }), 201)

        def delete(self, post_id):
            uuid = to_uuid(post_id)
            if uuid is None:
                return Response(f'invalid uuid {post_id}', status=400)

            result = post_collection.delete_one({'uuid': str(uuid)})
            if result.deleted_count == 0:
                return Response(f'{uuid} not found', status=404)

            return Response(f'deleted {uuid}', status=204)

        def put(self, post_id):
            uuid = to_uuid(post_id)
            if uuid is None:
                return Response(f'invalid uuid {post_id}', status=400)

            json_payload = request.get_json()
            if json_payload is None:
                return Response('no json payload', status=400)

            content, failure_reason = PostContent.from_api(json_payload)
            if content is None:
                return Response(failure_reason, status=400)

            post = Post(
                id=uuid,
                content=content,
            )
            result = post_collection.update_one({'uuid': str(uuid)}, {
                "$set": Post.to_database(post),
            })
            if result.matched_count == 0:
                return Response(f'{uuid} not found', status=404)

            return Response('updated', status=204)

    return PostAPI.as_view('post_api')


if __name__ == '__main__':
    client = MongoClient(username='root', password='root')

    post_view = create_post_api_view(client)
    app.add_url_rule('/post/', view_func=post_view, methods=['GET'], defaults={'post_id': None})
    app.add_url_rule('/post/', view_func=post_view, methods=['POST'])
    app.add_url_rule('/post/<string:post_id>', view_func=post_view,
                     methods=['GET', 'DELETE', 'PUT'])

    app.run()
