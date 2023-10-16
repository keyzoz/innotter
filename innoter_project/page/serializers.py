from rest_framework import serializers

from .models import Followers, Page, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):

    uuid = serializers.UUIDField(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=Tag.objects.all()
    )

    class Meta:
        model = Page
        fields = "__all__"
        extra_fields = {
            "followers": {"read_only": True},
            "image_url": {"required": False},
            "is_blocked": {"read_only": True},
            "unblock_date": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = ("uuid",)
