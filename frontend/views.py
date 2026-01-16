from django.shortcuts import render

def login_page(request):
    return render(request, "login.html")

def otp_page(request):
    return render(request, "otp.html")

def dashboard_super_admin(request):
    return render(request, "dashboard_super_admin.html")

def dashboard_admin(request):
    return render(request, "dashboard_admin.html")

def admins_page(request):
    return render(request, "admins.html")

def careers_page(request):
    return render(request, "careers.html")
