from django.urls import path

from . import views

urlpatterns = [
    path("v1/page/<int:page_id>", views.get_page_info, name="get_page_info"),
]
