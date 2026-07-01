from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('',                                views.overview,        name='overview'),
    path('users/',                          views.user_list,       name='users'),
    path('users/<int:user_id>/role/',       views.change_role,     name='change_role'),
    path('users/<int:user_id>/verify/',     views.verify_page,     name='verify_page'),
    path('moderation/',                     views.moderation_queue, name='moderation'),
    path('moderation/post/<int:post_id>/delete/',         views.delete_post,     name='delete_post'),
    path('moderation/listing/<int:listing_id>/remove/',   views.remove_listing,  name='remove_listing'),
    path('moderation/resource/<int:resource_id>/remove/', views.remove_resource, name='remove_resource'),
]