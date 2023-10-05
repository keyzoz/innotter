from django.urls import path

from . import views

urlpatterns = [
    path("v1/feed", views.get_feed, name="feed"),
]
