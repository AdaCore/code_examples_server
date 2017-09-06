# -*- coding: utf-8 -*-

import json

from rest_framework.response import Response
from rest_framework.decorators import api_view

from compile_server.app.models import Resource, Example


@api_view(['POST'])
def check_program(request):
    received_json = json.loads(request.body)

    matches = Example.objects.filter(name=received_json['example_name'])

    if not matches:
        return Response()

    e = matches[0]
    print received_json
    print e
    result = {'output': "bla\nbla\nbla"}
    return Response(result)
