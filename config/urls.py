from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/',       admin.site.urls),
    path('users/',       include('users.urls')),
    path('',             include('feed.urls')),
    path('messages/',    include('messaging.urls')),
    path('resources/',   include('resources.urls')),
    path('events/',      include('events.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('dashboard/',   include('dashboard.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
        'show_indexes': False,
    }),
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': False,
    }),
]