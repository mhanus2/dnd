from django.urls import path
from . import views


urlpatterns = [    
    path('', views.get_races, name='races'),
    path('update_races/', views.update_races, name='update-races'),
]

