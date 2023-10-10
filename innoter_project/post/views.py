from django.db import IntegrityError
from page.auth import CustomAuthentication
from page.models import Followers, Page
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


@authentication_classes([CustomAuthentication])
@api_view(["GET"])
def get_feed(request):
    followed_pages = Followers.objects.filter(user=request.user).values_list(
        "page_id", flat=True
    )
    posts = Post.objects.filter(page_id__in=followed_pages)

    serializer = PostSerializer(posts, many=True)
    serializer_data = serializer.data
    print(request.user)
    return Response(serializer_data, status=status.HTTP_200_OK)
