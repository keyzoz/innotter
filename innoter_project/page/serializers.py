from rest_framework import serializers

from .models import Page, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

    def create(self, validated_data):
        return Tag.objects.create(**validated_data)


class CreatePageSerializer(serializers.ModelSerializer):

    name = serializers.CharField()
    description = serializers.CharField()
    image_url = serializers.URLField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Page
        fields = ("name", "description", "image_url", "tags", "user")

    def create(self, validated_data):
        return Page.objects.create(**validated_data)


class PageListSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = ("id", "name", "user", "is_blocked")


class PageDetailSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    description = serializers.CharField()
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="tags")
    followers = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username"
    )

    class Meta:
        model = Page
        fields = ("name", "description", "tags", "user", "image_url", "followers")
