from rest_framework import serializers

from .models import Page, Tag


class PageListSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = ("id", "name", "user", "is_blocked")


class PageDetailSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    description = serializers.CharField()
    tags = serializers.SlugRelatedField(many=True, read_only=True)
    followers = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username"
    )

    class Meta:
        model = Page
        fields = ("name", "description", "tags", "user", "image_url", "followers")
