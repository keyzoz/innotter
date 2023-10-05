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
