# API application template using Django and GraphQL

## Getting started

Create `.env` file with `.env.example` keys in `config` folder.

Install dependencies:
```shell
poetry install
```

Make database migrations:
```shell
poetry run python manage.py migrate
```

Create superuser for admin panel access:
```shell
poetry run python manage.py createsuperuser
```

Run server:
```shell
poetry run python manage.py runserver
```
## Run tests
Run test and quality suits to make sure all dependencies are satisfied and applications works correctly before making changes.
```shell
python manage.py test
```
## Admin panel
With superuser credentials you can sign in admin panel `http://localhost:8000/admin/`

## Healthcheck
For check services (Database, AWS S3, etc.) running status 
follow to `http://localhost:8000/health/`

## GraphQL

For testing API you can follow the link `http://localhost:8000/graphql/`


