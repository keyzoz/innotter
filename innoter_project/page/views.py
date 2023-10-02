from rest_framework import generics
from rest_framework.views import APIView

from .models import Page, Tag
from .serializers import CreatePageSerializer, TagSerializer


class CreatePage(generics.CreateAPIView):
    queryset = Page.objects.all()
    serializer_class = CreatePageSerializer


class CreateTagView(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
