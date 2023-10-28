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
    path('<int:campaign_id>/characters/<int:character_id>/delete/', views.delete_character),

    path('<int:campaign_id>/characters/<int:character_id>/update/character-abilities/', views.update_character_abilities),
    path('<int:campaign_id>/characters/<int:character_id>/update/character-skills/', views.update_character_skills),
    path('<int:campaign_id>/characters/<int:character_id>/update/passive-skills/', views.update_passive_skills),
    path('<int:campaign_id>/characters/<int:character_id>/update/saving-throws/', views.update_saving_throws),
    path('<int:campaign_id>/characters/<int:character_id>/update/hit-dices/', views.update_hit_dices),
    path('<int:campaign_id>/characters/<int:character_id>/update/spell-slots/', views.update_spell_slots),

    path('<int:campaign_id>/characters/<int:character_id>/update-skills/', views.auto_update_character_skills),
    path('<int:campaign_id>/characters/<int:character_id>/update-abilities/', views.auto_update_character_abilities),
    path('<int:campaign_id>/characters/<int:character_id>/update-saving-throws/', views.update_saving_throws),
]
