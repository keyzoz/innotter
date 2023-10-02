from django.urls import path

from .views import CreatePage, CreateTagView

urlpatterns = [
    path("v1/pages", CreatePage.as_view()),
    path("v1/tag", CreateTagView.as_view()),
]
