ci: make-env run lint run-test

make-env:
	env > .env

run:
	sudo docker-compose up -d --build

lint:
	sudo docker exec python-base-graphql-api_web_1 flake8 users

run-test:
	sudo docker exec python-base-graphql-api_web_1 python3 manage.py test
