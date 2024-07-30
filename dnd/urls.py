from django.contrib import admin
from django.urls import include, path

# todo - add default page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("api_overview.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('campaigns/', include('campaigns.urls')),
    path('dnd_data/', include('dnd_data.urls')),
]
