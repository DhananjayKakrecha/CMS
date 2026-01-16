from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page),
    path("otp/", views.otp_page),

    path("dashboard/super-admin/", views.dashboard_super_admin),
    path("dashboard/admin/", views.dashboard_admin),

    path("admins/", views.admins_page),
    path("careers/", views.careers_page),
]
