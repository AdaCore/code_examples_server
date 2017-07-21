# code_examples_server

Prototype server for creating interactive "try SPARK / try Ada" webpages

## Getting started

To setup, do this:
```sh
virtualenv env
pip install -r REQUIREMENTS.txt
 ./manage.py makemigrations
 ./manage.py migrate
```

To enter some examples in the database, do this:
```sh
./manage.py fill_examples --dir=resources/example/a
```

To launch the server, do this:
```sh
./manage.py runserver
```
