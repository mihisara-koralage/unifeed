from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('feed.urls')),
    path('messages/', include('messaging.urls')),
    path('resources/', include('resources.urls')),
    path('events/', include('events.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('dashboard/', include('dashboard.urls')),
]