# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Program(models.Model):
    """That's a program for ya!"""

    # The code
    code = models.TextField()


class ToolOutput(models.Model):
    """The result on running a tool on a program"""

    # The exit code
    status = models.IntegerField()

    # The complete raw output
    output = models.TextField()


class Resource(models.Model):
    """This represents a file or a directory.
    """

    # Base name of the resource
    name = models.TextField()

    # The contents of the resource
    contents = models.TextField()

    # TODO: if necessary (not sure it is) we can add
    # fields to represent a hierarchy of resources.


class Example(models.Model):
    """One example to present to the user.
    """

    # The unique name of the example
    name = models.TextField(unique=True)

    # A description
    description = models.TextField()
