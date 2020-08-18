echo "CREATE"
UUID=$(curl -s -H "Content-Type: application/json" -d '{"weight":1, "size":2}' localhost:5000/post/ | jq -r .uuid)

echo "LIST"
curl -s localhost:5000/post/ | jq .

echo "GET"
curl -s "localhost:5000/post/$UUID" | jq .

echo "PUT"
curl -s -X PUT -H "Content-Type: application/json" -d '{"weight":3, "size":4}' "localhost:5000/post/$UUID" | jq -r .uuid

echo "GET"
curl -s "localhost:5000/post/$UUID" | jq .

echo "DELETE"
curl -s -X DELETE -H "Content-Type: application/json" "localhost:5000/post/$UUID" 

echo "LIST"
curl -s localhost:5000/post/ | jq .
