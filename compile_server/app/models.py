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


class Book(models.Model):
    """ The represents a book """

    # the directory in relation to resources/books
    # that has the resources for this book
    directory = models.TextField()

    # This is the name of the book formatted as a url subdomain
    # This is be the same name of the folder where the book lives under resources
    subpath = models.TextField()

    # A description of the book
    description = models.TextField()

    # the title of the book
    title = models.TextField()

    # the author of the book
    author = models.TextField()