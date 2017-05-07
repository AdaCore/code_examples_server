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
                                            ProgramSerializer)

from compile_server.app.models import Program


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


class ProgramSet(viewsets.ModelViewSet):
    """View/Edit"""
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


@api_view(['POST'])
def check_program(request):
    received_json = json.loads(request.body)
    p = Program(code=received_json['program'])
    serializer = ProgramSerializer(p)

    return Response(serializer.data)


@api_view(['GET'])
def examples(request):
    return Response()


@api_view(['GET'])
def example(request, name):
    return Response()
