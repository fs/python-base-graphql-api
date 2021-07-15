ci: build lint run-test

env-file:
	env > .env

build:
	sudo docker-compose up -d

lint:
	sudo docker exec -t python-base-graphql-api_web_1 flake8 users

run-test:
	sudo docker exec -t python-base-graphql-api_web_1 python3 manage.py test
