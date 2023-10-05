from django.core.paginator import EmptyPage, Paginator
from page.auth import get_username_from_token
from page.models import Followers, Page
from page.serializers import PageSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


@api_view(["GET"])
def get_feed(request):
    try:
        data = get_username_from_token(request)
        username = data["username"]
    except KeyError:
        return Response(data["error"], status=status.HTTP_401_UNAUTHORIZED)
    except Page.DoesNotExist:
        return Response({"error": "Page not found"}, status=status.HTTP_404_NOT_FOUND)

    followed_pages = Followers.objects.filter(user=username).values_list(
        "page_id", flat=True
    )
    posts = Post.objects.filter(page_id__in=followed_pages)

    serializer = PostSerializer(posts, many=True)
    serializer_data = serializer.data
    return Response(serializer_data, status=status.HTTP_200_OK)
