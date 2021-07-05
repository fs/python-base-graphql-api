# API application template using Django and GraphQL

## Getting started

Create `.env` file with `.env.example` keys

Setup virtual environment: 
```shell
python -m venv venv
```

Activate venv: 
```shell
.\venv\Scripts\activate # For Windows
source venv/bin/activate # For Linux and MacOS
```

Install dependencies:
```shell
pip install -r requirements.txt
```

Make database migrations:
```shell
python manage.py migrate
```

Create superuser for admin panel access:
```shell
python manage.py createsuperuser
```

Run server:
```shell
python manage.py runserver 0.0.0.0:8000
```


## GraphQL

For testing API you can follow the link `http://localhost:8000/graphql/`

