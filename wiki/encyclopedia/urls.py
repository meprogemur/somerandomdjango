from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.title, name="title"),
    path("page/", views.page, name="page"),
    path("random/", views.ran, name="random"),
    path("search/", views.search, name="find"),
    path("<str:ed>/", views.edit, name="edit")
]
