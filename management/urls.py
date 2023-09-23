from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_management_tools, name='management'),
    path('update-races/', views.update_races, name='update-races'),
    path('update-character-classes/', views.update_character_classes, name='update-character-classes'),
    path('update-backgrounds/', views.update_backgrounds, name='update-backgrounds'),
    path('update-alignments/', views.update_alignments, name='update-alignments'),

]