docker stop $(docker ps -a -q --filter ancestor=redis --format="{{.ID}}") > /dev/null
docker run --rm -d -p 6379:6379 redis > /dev/null
python fake_data.py