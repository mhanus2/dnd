from django.urls import path
from . import views


urlpatterns = [    
    path('races/', views.get_races, name='races'),
]

