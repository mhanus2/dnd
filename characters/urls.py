from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_characters),
    path('campaign/<int:campaign_id>/', views.get_campaign_characters),

    path('<int:character_id>/', views.get_character_detail),
    
    path('create/', views.create_character),
    path('update/<int:character_id>', views.update_character_detail)
]