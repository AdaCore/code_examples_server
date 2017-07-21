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
                                            ResourceSerializer)

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


@api_view(['POST'])
def check_program(request):
    received_json = json.loads(request.body)
    p = Program(code=received_json['program'])
    serializer = ProgramSerializer(p)

    return Response(serializer.data)


@api_view(['GET'])
def examples(request):
    """Return a list of example names and their description"""
    examples = Example.objects.all()
    results = []
    for e in examples:
        results.append({'name': e.name, 'description': e.description})

    return Response(results)


@api_view(['GET'])
def example(request, name):
    # TODO: create an example serializer
    # TODO: catch case where the example does not exist
    e = Example.objects.filter(name=name)[0]
    resources = []
    for r in e.resources.all():
        serializer = ResourceSerializer(r)
        resources.append(serializer.data)
    # TODO: add example metadata to the result
    result = {'resources': resources}
    return Response(result)
