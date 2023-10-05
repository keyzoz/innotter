from rest_framework import serializers

from .models import Followers, Page, Tag


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
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Page
        fields = ("name", "description", "image_url", "tags", "user")


class PageSerializer(serializers.ModelSerializer):

    user = serializers.CharField(read_only=True)
    description = serializers.CharField()

    class Meta:
        model = Page
        fields = ("name", "description", "user", "image_url", "tags", "followers")


class PagePatchSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    image_url = serializers.URLField()
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Page
        fields = ("name", "description", "image_url", "tags")
