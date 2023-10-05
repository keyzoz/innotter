from django.urls import path

from . import views

urlpatterns = [
    path("v1/feed", views.get_feed, name="feed"),
    path("v1/page/<int:page_id>/post", views.create_post, name="create_post"),
]
