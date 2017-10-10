# code_examples_server

Prototype server for creating interactive "try SPARK / try Ada" webpages

## Getting started

To setup, do this:
```sh

# This is to create the virtualenv and install Python stuff
virtualenv env
source env/bin/activate
pip install -r REQUIREMENTS.txt

# This is to initialize the django database
 ./manage.py migrate

# This is to get the ACE editor
cd compile_server/app/static
git clone https://github.com/ajaxorg/ace-builds.git
```

To enter the environment, to this
```sh
source env/bin/activate
```

To enter some examples in the database, do this:
```sh
./manage.py fill_examples --dir=resources/example/hello_world
```

To launch the server, do this:
```sh
./manage.py runserver
```
