# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

import os
import yaml

from django.conf import settings

from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from compile_server.app.serializers import (UserSerializer,
                                            GroupSerializer,
                                            ResourceSerializer,
                                            ExampleSerializer,
                                            BookSerializer)

from compile_server.app.models import Resource, Example, Book


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
    booklist = {'books': Book.objects.all}
    return render(request, 'book_list.html', booklist)


def book_router(request, subpath):
    resources_base_path = os.path.join(settings.RESOURCES_DIR, "books")

    matches = Book.objects.filter(subpath=subpath)
    if not matches:
        booklist = {'books': Book.object.all}
        return render(request, 'book_list.html', booklist)

    bk = matches[0]
    serializer = BookSerializer(bk)

    book = serializer.data

    # open chapters list of book
    with open(os.path.join(book['directory'], "chapters.yaml"), 'r') as f:
        try:
            bookdata = yaml.load(f.read())
        except:
            print format_traceback
            print 'Could not decode yaml in {}'.format(book['directory'])
            return

    # store chapters and parts list in htmldata
    htmldata = bookdata
    htmldata['book_info'] = book

    # strip chapters out of list into new list for prev, next references
    chapter_list = []
    for p in bookdata['parts']:
        chapter_list.extend(p['chapters'])

    paginator = Paginator(chapter_list, 1)
    page = request.GET.get('page', 1)

    try:
        chapter_obj = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        chapter_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        chapter_obj = paginator.page(paginator.num_pages)

    htmldata['chapter_obj'] = chapter_obj

    chapter = chapter_obj.object_list[0]

    mdcontent_page = os.path.join(book['directory'],
                                "pages",
                                "%s.md" % (chapter["url"]))
    rstcontent_page = os.path.join(book['directory'],
                                  "pages",
                                  "%s.rst" % (chapter["url"]))

    # check for markdown version
    if os.path.isfile(mdcontent_page):
        with open(mdcontent_page, 'r') as f:
            htmldata['mdcontent'] = f.read()
    elif os.path.isfile(rstcontent_page):
        with open(rstcontent_page, 'r') as f:
            htmldata['rstcontent'] = f.read()
    else:
        with open(os.path.join(resources_base_path,
                               "under-construction.md")) as f:
            htmldata['mdcontent'] = f.read()

    if request.is_ajax():
        template = 'readerpage.html'
    else:
        template = 'book_sidebar.html'

    return render(request, template, htmldata)
