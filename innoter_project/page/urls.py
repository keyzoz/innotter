from django.urls import include, path
from rest_framework import routers

from . import views

pages_router = routers.DefaultRouter()
pages_router.register("page", views.PageViewSet, basename="pages")
pages_router.register("tag", views.TagView, basename="tags")


urlpatterns = [path("", include(pages_router.urls))]
