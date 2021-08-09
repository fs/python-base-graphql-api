ci: build lint run-test

env-file:
	env > .env

build:
	sudo docker-compose --env-file config/.env up -d

lint:
	sudo docker exec -t python-base-graphql-api_web_1 poetry run flake8 server/apps/users

run-test:
	sudo docker exec -t python-base-graphql-api_web_1 poetry run python3 manage.py test
