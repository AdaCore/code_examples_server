# code_examples_server

Prototype server for creating interactive "try SPARK / try Ada" webpages

## Requirements

This project requires Vagrant and VirtualBox

## Getting started

To setup run:
```
$ vagrant up
$ vagrant ssh

# From the vagrant VM run:

$ cd /vagrant
$ ./manage.py runserver 0.0.0.0
```

At this point you can point your browser on your host machine to 127.0.0.1:8000 to get to the code_examples_server index page or build the learn repo in local mode to point the widgets at localhost:8000

## DB operations
To enter some examples in the database, do this:
```sh
./manage.py fill_examples --dir=resources/example/hello_world
```

To enter many examples in the database where the examples are listed in a yaml file, do this:
```sh
./manage.py fill_examples --conf=resources/test_conf.yaml
```
