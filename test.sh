echo "CREATE"
UUID=$(curl -s 'http://localhost:5000/graphql?' \
  -H 'Content-Type: application/json' \
  --data-binary '{"query":"mutation {upsertPost(size:1.0, weight: 2.0) {post {uuid}}}","variables":null}' | jq -r .data.upsertPost.post.uuid)
echo "New profile created $UUID"

echo "LIST"
curl -s 'http://localhost:5000/graphql?' \
  -H 'Content-Type: application/json' \
  --data-binary '{"query":"query {posts(postFilter:{}) {uuid\nweight\nsize}}","variables":null}' | jq .

echo "GET"
curl -s 'http://localhost:5000/graphql?' \
  -H 'Content-Type: application/json' \
  --data-binary '{"query":"query {posts(postFilter:{uuid:\"'"$UUID"'\"}) {uuid\nweight\nsize}}","variables":null}' | jq .

echo "UPDATE"
curl -s 'http://localhost:5000/graphql?' \
  -H 'Content-Type: application/json' \
  --data-binary '{"query":"mutation {upsertPost(size:41.0, weight: 42.0, uuid:\"'"$UUID"'\") {post {uuid\nweight\nsize}}}","variables":null}' | jq -r .

echo "GET"
curl -s 'http://localhost:5000/graphql?' \
  -H 'Content-Type: application/json' \
  --data-binary '{"query":"query {posts(postFilter:{uuid:\"'"$UUID"'\"}) {uuid\nweight\nsize}}","variables":null}' | jq .

echo "DELETE"
curl  -s 'http://localhost:5000/graphql?' \
  -H 'Content-Type: application/json' \
  --data-binary '{"query":"mutation {deletePost(uuid: \"'"$UUID"'\") {ok}}","variables":null}' | jq .

echo "LIST"
curl -s 'http://localhost:5000/graphql?' \
  -H 'Content-Type: application/json' \
  --data-binary '{"query":"query {posts(postFilter:{}) {uuid\nweight\nsize}}","variables":null}' | jq .
