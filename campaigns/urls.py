from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_campaigns),
    path('<int:campaign_id>/', views.get_campaign_detail, name='campaign-detail'),
    path('update-campaign/<int:campaign_id>/', views.update_campaign_detail, name='update-campaign'),
    path('delete-campaign/<int:campaign_id>/', views.delete_campaign_detail, name='delete-campaign')
]