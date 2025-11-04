from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("register/", views.register),      # POST
    path("login/", views.login),            # POST
    path("logout/", views.logout),          # POST (blacklist refresh)
    path("refresh/", TokenRefreshView.as_view()),  # POST
    path("me/", views.me),                  # GET (protected)
]
