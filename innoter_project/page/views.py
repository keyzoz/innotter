from django.core.paginator import EmptyPage, Paginator
from post.models import Post
from post.serializers import PostSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response

from .auth import CustomAuthentication
from .models import Page
from .serializers import PageSerializer


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
