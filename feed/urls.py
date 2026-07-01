from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('',              views.feed_home,    name='home'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('tag/<str:tag_name>/', views.hashtag_feed, name='hashtag'),
]