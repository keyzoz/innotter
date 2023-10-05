from django.core.paginator import EmptyPage, Paginator
from page.models import Page
from page.serializers import PageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


@api_view(["GET"])
def get_page_info(request, page_id):
    try:
        page = Page.objects.get(id=page_id)
    except Exception as err:
        return Response({"error": str(err)}, status=404)

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
