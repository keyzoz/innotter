from rest_framework import serializers

from .models import Followers, Page, Tag


class PageSerializer(serializers.ModelSerializer):

    user = serializers.CharField(read_only=True)

    class Meta:
        model = Page
        fields = "__all__"
        extra_fields = {
            "tags": {"required": False},
            "followers": {"read_only": True},
            "image_url": {"required": False},
            "is_blocked": {"read_only": True},
            "unblock_date": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = "__all__"
