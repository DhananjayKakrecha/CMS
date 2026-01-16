from django.urls import path
from .views import (
    AdminListView,
    AdminCreateView,
    AdminUpdateView,
    AdminDeleteView,
    AdminAccessToggleView,
)

urlpatterns = [
    path("admins/", AdminListView.as_view()),
    path("admins/create/", AdminCreateView.as_view()),
    path("admins/<uuid:admin_id>/update/", AdminUpdateView.as_view()),
    path("admins/<uuid:admin_id>/delete/", AdminDeleteView.as_view()),
    path("admins/<uuid:admin_id>/toggle-access/", AdminAccessToggleView.as_view()),
]
