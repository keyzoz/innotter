from django.urls import path

from . import views

urlpatterns = [
    path("feed", views.get_feed, name="feed"),
]
