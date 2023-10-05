from django.urls import path

from . import views

urlpatterns = [
    path("v1/pages", views.create_page, name="create_page"),
    path("v1/tag", views.create_tag, name="create_tag"),
    path("v1/page/<int:page_id>", views.patch_page, name="patch_page"),
]
