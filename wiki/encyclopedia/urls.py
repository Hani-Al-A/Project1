from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("createPage", views.createPage, name="createPage"),
    path("editPage/<str:title>", views.editPage, name="editPage"),
    path("random", views.randomiser, name="randomiser")
]
