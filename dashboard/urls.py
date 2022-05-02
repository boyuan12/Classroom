from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_all_classrooms),
    path("create/", views.create_classroom),
    path("join/", views.join_classroom),
]