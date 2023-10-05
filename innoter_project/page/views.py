from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .auth import get_username_from_token
from .models import Page
from .serializers import (CreatePageSerializer, PagePatchSerializer,
                          TagSerializer)


@api_view(["POST"])
def create_page(request):
    data = get_username_from_token(request)
    try:
        username = data["username"]
    except KeyError:
        return Response(data["error"], status=status.HTTP_401_UNAUTHORIZED)
    serializer = CreatePageSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(user=username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                "Inaccurate data inputs", status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_tag(request):
    data = get_username_from_token(request)
    try:
        _ = data["username"]
    except KeyError:
        return Response(data["error"], status=status.HTTP_401_UNAUTHORIZED)
    serializer = TagSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                "Inaccurate data inputs", status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def patch_page(request, page_id):
    data = get_username_from_token(request)
    try:
        username = data["username"]
        page = Page.objects.get(id=page_id)
        if page.user != username:
            return Response(
                {"error": "You're not a owner of this page"}, status.HTTP_403_FORBIDDEN
            )
    except KeyError:
        return Response(data["error"], status=status.HTTP_401_UNAUTHORIZED)
    except Page.DoesNotExist:
        return Response({"error": "Page not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        serializer = PagePatchSerializer(page, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
