from django.urls import path

from . import views
from .views import csrf_check, custom_login

urlpatterns = [
    path('', views.get_api_overview),
    path('csrf-check/', csrf_check, name='csrf_check'),
    path('login/', custom_login, name='login'),
]
