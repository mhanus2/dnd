from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_campaigns),
    path('<int:campaign_id>/', views.get_campaign_detail),
    
    path('create/', views.create_campaign),
    path('update/<int:campaign_id>/', views.update_campaign),
    path('delete/<int:campaign_id>/', views.delete_campaign),
]