# depot/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('depots/', views.list_depots, name='list_depots'),
    path('depot-nearby/', views.nearest_depot, name='nearest_depot'),
    path('depot-nearest-route/', views.nearest_depot_route, name='nearest_depot_route'),
]
