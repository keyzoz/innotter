from django.core.paginator import EmptyPage, Paginator
from post.models import Post
from post.serializers import PostSerializer
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .auth import CustomAuthentication
from .models import Followers, Page, Tag
from .serializers import PageSerializer, TagSerializer


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    authentication_classes = [CustomAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            page = Page.objects.get(id=kwargs.get("pk"))
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

    @action(detail=True, methods=["patch"])
    def follow(self, request, pk=None):
        try:
            Followers.objects.get(page_id_id=pk, user=request.user)
        except Followers.DoesNotExist:
            try:
                follow = Followers(page_id_id=pk, user=request.user)
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
            follow = Followers.objects.get(page_id_id=pk, user=request.user)
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
        return Response({"message": "Unfollowed"}, status=status.HTTP_201_CREATED)


class TagView(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [CustomAuthentication]
