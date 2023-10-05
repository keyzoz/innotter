from django.core.paginator import Paginator
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .auth import get_username_from_token
from .models import Page
from .serializers import CreatePageSerializer, TagSerializer


@api_view(["POST"])
def create_page(request):
    data = get_username_from_token(request)
    try:
        username = data["username"]
    except KeyError:
        return Response(data["error"], status=401)
    serializer = CreatePageSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(user=username)
            return Response(serializer.data, status=201)
        except IntegrityError:
            return Response("Inaccurate data inputs", status=412)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def create_tag(request):
    data = get_username_from_token(request)
    try:
        _ = data["username"]
    except KeyError:
        return Response(data["error"], status=401)
    serializer = TagSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=201)
        except IntegrityError:
            return Response("Inaccurate data inputs", status=412)
    return Response(serializer.errors, status=400)
