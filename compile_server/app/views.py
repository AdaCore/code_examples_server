# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from bs4 import BeautifulSoup
import docutils
import markdown
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


def md_filter(text):
    return markdown.markdown(text)


def rst_filter(text):
    return docutils.core.publish_parts(text, writer_name='html')['html_body']


def toc_filter(htmldata):
    def append_li(ul, i, h):
        h['id'] = "header" + str(i)
        new_link_tag = toc_soup.new_tag('a', href='#')
        new_link_tag.string = h.string
        new_link_tag['class'] = "toc-link pure-menu-link"
        new_link_tag['id'] = "hlink" + str(i)

        new_li_tag = toc_soup.new_tag('li')
        new_li_tag['class'] = "pure-menu-item"
        new_li_tag.append(new_link_tag)
        ul.append(new_li_tag)

    def append_ul(ul):
        new_ul = toc_soup.new_tag('ul')
        new_ul['class'] = "pure-menu-list"
        ul.append(new_ul)
        return new_ul


    prev_level = 1

    reader_soup = BeautifulSoup(htmldata['content'], "html.parser")
    toc_soup = BeautifulSoup(htmldata['sidebar'], "html.parser")

    current_ul = toc_soup.ul

    headers = reader_soup.find_all(['h1', 'h2'])

    for i, h in enumerate(headers):
        cur_level = int(h.name[1:])

        if cur_level < prev_level:
            outer_ul = current_ul.find_parent('ul')
            if outer_ul is not None:
                prev_level = cur_level
                current_ul = outer_ul

        elif cur_level > prev_level:
            prev_level = cur_level
            current_ul = append_ul(current_ul)

        append_li(current_ul, i, h)


    htmldata['content'] = str(reader_soup)
    htmldata['sidebar'] = str(toc_soup)
    return htmldata


def book_router(request, subpath):
    resources_base_path = os.path.join(settings.RESOURCES_DIR, "books")

    matches = Book.objects.filter(subpath=subpath)
    if not matches:
        booklist = {'books': Book.object.all}
        return render(request, 'book_list.html', booklist)

    bk = matches[0]
    serializer = BookSerializer(bk)

    book = serializer.data

    # open book info
    with open(os.path.join(book['directory'], "info.yaml"), 'r') as f:
        try:
            bookdata = yaml.load(f.read())
        except:
            print format_traceback
            print 'Could not decode yaml in {}'.format(book['directory'])
            return

    # store chapters and parts list in htmldata
    htmldata = {}
    htmldata['book_info'] = book

    htmldata['content'] = ''

    htmldata['sidebar'] = '<ul class="pure-menu-list"></ul>'

    # get list of pages from info.yaml, convert to html, and concat into string
    for page in bookdata['pages']:
        filepath = os.path.join(book['directory'], page)
        filename, file_ext = os.path.splitext(filepath)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
                if file_ext == '.md':
                    htmldata['content'] += md_filter(content)
                elif file_ext == '.rst':
                    htmldata['content'] += rst_filter(content)
        else:
            with open(os.path.join(resources_base_path, "under-construction.md")) as f:
                htmldata['content'] += md_filter(f.read())

    htmldata = toc_filter(htmldata)

    return render(request, 'readerpage.html', htmldata)
