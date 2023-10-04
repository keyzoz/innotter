from django.urls import path

from . import views

urlpatterns = [
    path("v1/pages", views.create_page, name="create_page"),
    path("v1/tag", views.create_tag, name="create_tag"),
]
