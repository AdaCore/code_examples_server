#!/usr/bin/env bash

# Install system deps
apt-get update
apt-get install -y \
    python2.7 \
    python-pip \
    lxc \
    lxd \
    lxd-client \
    make

# Initialize lxc for code_examples_server
lxd init --auto

# Install code_examples_server deps
cd /vagrant
pip install -r REQUIREMENTS.txt
cd infrastructure
make

cd /vagrant
./manage.py migrate
./manage.py fill_examples --dir=resources/templates/ada_main
./manage.py fill_examples --dir=resources/templates/inline_code
./manage.py fill_examples --dir=resources/templates/simple_main
./manage.py fill_examples --dir=resources/templates/spark_main
