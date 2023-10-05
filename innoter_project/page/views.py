from django.core.paginator import EmptyPage, Paginator
from django.db import IntegrityError
from post.models import Post
from post.serializers import PostSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import get_username_from_token
from .models import Followers, Page
from .serializers import (CreatePageSerializer, PagePatchSerializer,
                          PageSerializer, TagSerializer)


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


class PageDetailView(APIView):
    @staticmethod
    def get(request, page_id):
        try:
            data = get_username_from_token(request)
            page = Page.objects.get(id=page_id)
        except KeyError:
            return Response(data["error"], status=status.HTTP_401_UNAUTHORIZED)
        except Page.DoesNotExist:
            return Response(
                {"error": "Page not found"}, status=status.HTTP_404_NOT_FOUND
            )

        page_number = request.query_params.get("page", 1)
        limit = request.query_params.get("limit", 30)

        posts = Post.objects.filter(page=page, reply_to=None)
        paginator = Paginator(posts, limit)

        try:
            page_posts = paginator.page(page_number)
        except EmptyPage:
            return Response({"error": "No more pages available"}, status=400)

        serializer = PageSerializer(page)
        serializer_data = serializer.data

        serializer_data["posts"] = PostSerializer(page_posts, many=True).data

        return Response(serializer_data)

    @staticmethod
    def patch(request, page_id):
        data = get_username_from_token(request)
        try:
            username = data["username"]
            page = Page.objects.get(id=page_id)
            if page.user != username:
                return Response(
                    {"error": "You're not a owner of this page"},
                    status.HTTP_403_FORBIDDEN,
                )
        except KeyError:
            return Response(data["error"], status=status.HTTP_401_UNAUTHORIZED)
        except Page.DoesNotExist:
            return Response(
                {"error": "Page not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.method == "PATCH":
            serializer = PagePatchSerializer(page, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def follow_page(request, page_id):
    data = get_username_from_token(request)
    try:
        username = data["username"]
        Followers.objects.get(page_id_id=page_id, user=username)
    except KeyError:
        return Response(data["error"], status=status.HTTP_401_UNAUTHORIZED)
    except Followers.DoesNotExist:
        try:
            follow = Followers(page_id_id=page_id, user=username)
            follow.save()
            Page.objects.get(id=page_id).followers.add(follow)
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({"message": "Followed"}, status=status.HTTP_201_CREATED)
    return Response(
        {"error": "You're already followed on this page"},
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@api_view(["POST"])
def unfollow_page(request, page_id):
    data = get_username_from_token(request)
    try:
        username = data["username"]
        follow = Followers.objects.get(page_id_id=page_id, user=username)
    except KeyError:
        return Response(data["error"], status=status.HTTP_401_UNAUTHORIZED)
    except Followers.DoesNotExist:
        return Response(
            {"error": "You're not follower of this page"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    try:
        follow.delete()
    except Exception as err:
        return Response(
            {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response({"message": "Unfollowed"}, status=status.HTTP_200_OK)
