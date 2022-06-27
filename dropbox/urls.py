from django.urls import path
from . import views

urlpatterns = [
    path("authorize/", views.dropbox_oauth),
    path("authorized/", views.dropbox_authorized),
    path("search/", views.search_files),
    path("api-search-file/", views.search_files_api)
]