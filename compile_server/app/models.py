# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


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
    basename = models.TextField()

    # The contents of the resource if it is a file
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

    # The directory which contains the original contents
    original_dir = models.TextField()

    # The name of the main
    main = models.TextField()

    # An example is a contains a set of resources
    resources = models.ManyToManyField(Resource)


class ProgramRun(models.Model):
    """Represents programs currently being run"""

    working_dir = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
