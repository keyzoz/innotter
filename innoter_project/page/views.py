from datetime import timedelta

from django.core.paginator import EmptyPage, Paginator
from django.db import IntegrityError
from django.utils import timezone
from permissions import IsAdminOrModeratorOfOwnerGroup, IsOwnerOfPage
from post.models import Post
from post.serializers import PostSerializer
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .auth import CustomAuthentication
from .models import Followers, Page, Tag
from .serializers import FollowersSerializer, PageSerializer, TagSerializer


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    authentication_classes = [CustomAuthentication]

    permission_classes_by_action = {
        "partial_update": [IsOwnerOfPage],
        "update": [IsOwnerOfPage],
        "destroy": [IsAdminOrModeratorOfOwnerGroup],
        "followers": [IsAdminOrModeratorOfOwnerGroup],
        "block": [IsAdminOrModeratorOfOwnerGroup],
        "post": [IsOwnerOfPage],
    }

    def perform_create(self, serializer):
        serializer.save(uuid=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        page = self.get_object()

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

    @action(detail=True, methods=["patch"])
    def follow(self, request, pk=None):
        try:
            Followers.objects.get(page_id_id=pk, uuid=request.user)
        except Followers.DoesNotExist:
            try:
                follow = Followers(page_id_id=pk, uuid=request.user)
                follow.save()
                Page.objects.get(id=pk).followers.add(follow)
            except Exception as err:
                return Response(
                    {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return Response({"message": "Followed"}, status=status.HTTP_201_CREATED)
        return Response(
            {"error": "You're already followed on this page"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @action(detail=True, methods=["patch"])
    def unfollow(self, request, pk=None):
        try:
            follow = Followers.objects.get(page_id_id=pk, uuid=request.user)
        except Page.DoesNotExist:
            return Response(
                {"error": "Page not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            follow.delete()
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({"message": "Unfollowed"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def followers(self, request, pk=None):
        try:
            followers = Page.objects.get(id=pk).followers.all()
        except Page.DoesNotExist:
            return Response(
                {"error": "You're not follower of this page"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        serializer = FollowersSerializer(followers, many=True)
        users = serializer.data
        if users:
            return Response(serializer.data)
        return Response({"detail": "The list of users is empty"})

    @action(detail=True, methods=["patch"])
    def block(self, request, pk=None):
        page = self.get_object()
        hours_to_block = request.data.get("hours_to_block")

        try:
            hours_to_block = int(hours_to_block)
        except ValueError:
            return Response(
                {"error": "Invalid hours format"}, status=status.HTTP_400_BAD_REQUEST
            )

        unblock_date = timezone.now() + timedelta(hours=hours_to_block)
        page.is_blocked = True
        page.unblock_date = unblock_date
        page.save()
        return Response(
            {"message": "Page blocked successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def post(self, request, pk=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(page_id=pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    "Inaccurate data inputs",
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class TagView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [CustomAuthentication]
