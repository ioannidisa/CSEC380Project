docker-compose -f docker-compose.yml up --build -d
echo 'Migrating Database'
sleep 10
docker exec python ./manage.py migrate
docker exec python ./manage.py collectstatic --no-input
echo 'Server listening on port 4000; reachable from http://localhost:4000'