from page.serializers import PageSerializer
from rest_framework import serializers

from .models import Likes, Post


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    likes = LikesSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class CreatePostSerializer(serializers.ModelSerializer):
    page = PageSerializer(read_only=True)
    reply_to = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Post
        fields = ("page", "content", "reply_to")
