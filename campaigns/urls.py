from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_campaigns),
    path('<int:campaign_id>/', views.get_campaign_detail),

    path('create/', views.create_campaign),
    path('update/<int:campaign_id>/', views.update_campaign),
    path('delete/<int:campaign_id>/', views.delete_campaign),

    path('<int:campaign_id>/characters/', views.get_characters),
    path('<int:campaign_id>/characters/<int:character_id>/', views.get_character_detail),

    path('<int:campaign_id>/characters/create/', views.create_character),
    path('<int:campaign_id>/characters/update/<int:character_id>', views.update_character),
    path('<int:campaign_id>/characters/delete/<int:character_id>', views.delete_character)
]
