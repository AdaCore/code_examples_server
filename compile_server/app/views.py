# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User, Group
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
