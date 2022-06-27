from django.urls import path
from . import views

urlpatterns = [
    path("authorize/", views.dropbox_oauth),
    path("authorized/", views.dropbox_authorized),
    path("files/", views.search_files)
]