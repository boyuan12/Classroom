from django.urls import path
from . import views

urlpatterns = [
    path("<str:class_id>/", views.index),
    path("<str:class_id>/classwork/new/", views.post_assignment),
    path("<str:class_id>/classwork/", views.view_assignments),
    path("<str:class_id>/assignment/<str:assignment_slug>/", views.view_assignment),
    path("<str:class_id>/assignment/<str:assignment_slug>/delete/", views.delete_submission_api)
]