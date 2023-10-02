from innoter_project.page.models import Tag, Page
from rest_framework import serializers


class PageListSerializer(serializers.ModelSerializer):

    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = ("id", "name", "user", "is_blocked")