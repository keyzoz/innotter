from django.urls import include, path
from rest_framework import routers

from . import views

posts_router = routers.DefaultRouter()
posts_router.register("post", views.PostViewSet, basename="posts")
urlpatterns = [
    path("", include(posts_router.urls)),
    path("feed", views.get_feed, name="feed"),
]
