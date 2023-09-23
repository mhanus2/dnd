from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_characters, name='characters'),
    path('<int:character_id>/', views.get_character_detail, name='character-detail'),
]