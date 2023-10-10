from page.serializers import PageSerializer
from rest_framework import serializers

from .models import Likes, Post


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    page = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        extra_fields = {
            "page": {"read_only": True},
            "reply_to": {"required": False},
            "likes": {"required": False, "read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }
