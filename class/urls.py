from django.urls import path
from . import views

urlpatterns = [
    path("<str:class_id>/", views.index),
    path("<str:class_id>/classwork/new/", views.post_assignment),
]