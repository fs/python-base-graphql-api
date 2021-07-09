ci: make-env update-requirements lint run-test

make-env:
	env > .env

lint:
	sudo docker exec python-base-graphql-api_web_1 flake8

run-test:
	sudo docker exec python-base-graphql-api_web_1 python3 manage.py test

update-requirements:
	sudo docker exec python-base-graphql-api_web_1 pip3 install -r requirements.txt
