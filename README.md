# code_examples_server

Prototype server for creating interactive "try SPARK / try Ada" webpages

## Requirements

In addition to Python, this system relies on LXC to sandbox
the run of executables. To do this, you need
  - a container named "safecontainer"
  - this container should have a non-admin user 'ubuntu'

## Getting started

To setup, do this:
```sh

# This is to create the virtualenv and install Python stuff
virtualenv env
source env/bin/activate
pip install -r REQUIREMENTS.txt

# This is to initialize the django database
 ./manage.py migrate

```

To enter the environment, to this
```sh
source env/bin/activate
```

To enter some examples in the database, do this:
```sh
./manage.py fill_examples --dir=resources/example/hello_world
```

To enter many examples in the database where the examples are listed in a yaml file, do this:
```sh
./manage.py fill_examples --conf=resources/test_conf.yaml
```

To launch the server, do this:
```sh
./manage.py runserver
```
