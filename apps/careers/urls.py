from django.urls import path
from .views import (
    CareerCMSListView,
    CareerCreateView,
    CareerUpdateView,
    CareerDeleteView,
    CareerPublicListView
)

urlpatterns = [
    path("cms/", CareerCMSListView.as_view()),
    path("cms/create/", CareerCreateView.as_view()),
    path("cms/<uuid:career_id>/update/", CareerUpdateView.as_view()),
    path("cms/<uuid:career_id>/delete/", CareerDeleteView.as_view()),
    path("public/", CareerPublicListView.as_view()),
]
