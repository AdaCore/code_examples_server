# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

import os
import yaml

from django.conf import settings

from django.contrib.auth.models import User, Group
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from compile_server.app.serializers import (UserSerializer,
                                            GroupSerializer,
                                            ResourceSerializer,
                                            ExampleSerializer)

from compile_server.app.models import Resource, Example


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ResourceSet(viewsets.ModelViewSet):
    """View/Edit"""
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


def CrossDomainResponse(data=None):
    """Return a response which accepts cross-domain queries"""
    r = Response(data)
    r["Access-Control-Allow-Origin"] = "*"
    return r


@api_view(['GET'])
def examples(request):
    """Return a list of example names and their description"""
    examples = Example.objects.all()
    results = []
    for e in examples:
        results.append({'name': e.name, 'description': e.description})

    return CrossDomainResponse(results)


@api_view(['GET'])
def example(request, name):
    # TODO: create an example serializer
    matches = Example.objects.filter(name=name)
    if not matches:
        return CrossDomainResponse()

    e = matches[0]
    resources = []
    for r in e.resources.all():
        serializer = ResourceSerializer(r)
        resources.append(serializer.data)

    result = {'name': e.name,
              'description': e.description,
              'main': e.main,
              'resources': resources}
    return CrossDomainResponse(result)


def code_page(request, example_name):
    matches = Example.objects.filter(name=example_name)
    if not matches:
        return Response()

    e = matches[0]
    serializer = ExampleSerializer(e)
    context = {'example': serializer.data}
    return render(request, 'code_page.html', context)


@xframe_options_exempt
def code_embed(request, example_name):
    matches = Example.objects.filter(name=example_name)
    if not matches:
        return Response()

    e = matches[0]
    serializer = ExampleSerializer(e)
    context = {'example': serializer.data}
    return render(request, 'code_embed.html', context)


def examples_list(request):
    context = {'examples': Example.objects.all}
    return render(request, 'examples_list.html', context)


def book_list(request):
    resources_base_path = os.path.join(settings.RESOURCES_DIR, "books")

    with open(os.path.join(resources_base_path, "book_list.yaml"), 'r') as f:
        booklist = yaml.load(f)
    return render(request, 'book_list.html', booklist)


def book_router(request, book, part, chapter):
    resources_base_path = os.path.join(settings.RESOURCES_DIR, "books")
    book_path = os.path.join(resources_base_path, book)

    with open(os.path.join(resources_base_path, "book_list.yaml"), 'r') as f:
        booklist = yaml.load(f)

    # If the book url is not valid, jump back to book list
    if not os.path.isdir(book_path):
        return render(request, 'book_list.html', booklist)

    path = os.path.join(book_path, "chapters.yaml")

    # open chapters list of book
    with open(path, 'r') as f:
        bookdata = yaml.load(f)

    # store chapters and parts list in htmldata
    htmldata = bookdata

    # store book url and book title for side bar and absolute path references
    for b in booklist['books']:
        if b['url'] == book:
            htmldata['book_title'] = b['title']
    htmldata['book_url'] = book

    # store chapter and part numbers for absolute links
    htmldata['sel_part'] = int(part)
    htmldata['sel_chapter'] = int(chapter)

    # strip chapters out of list into new list for prev, next references
    chapter_list = []
    for p in bookdata['parts']:
        chapter_list.extend(p['chapters'])

    # search list for current, prev, and next chapter references
    val_search = "part%s-chapter%s" % (part, chapter)

    inrange = False
    for i, ch in enumerate(chapter_list):
        if ch['url'] == val_search:
            inrange = True
            htmldata['sel_topic'] = ch
            if i != 0:
                htmldata['prev_topic'] = chapter_list[i - 1]
            if i != len(chapter_list) - 1:
                htmldata['next_topic'] = chapter_list[i + 1]
            break

    # load page, if part or chapter is out of range go to unknown page link
    if inrange:
        content_page = os.path.join(book_path,
                                    "pages",
                                    "part%s-chapter%s.md" % (part, chapter))

        if os.path.isfile(content_page):
            with open(content_page, 'r') as f:
                htmldata['content'] = f.read()
        else:
            with open(os.path.join(resources_base_path,
                                   "under-construction.md")) as f:
                htmldata['content'] = f.read()
    else:
        with open(os.path.join(resources_base_path,
                               "invalid-page.md")) as f:
            htmldata['content'] = f.read()

    return render(request, 'readerpage.html', htmldata)
