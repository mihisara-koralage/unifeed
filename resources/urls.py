from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('',           views.resource_list,   name='list'),
    path('submit/',    views.submit_resource,  name='submit'),
    path('<int:resource_id>/open/', views.open_resource, name='open'),
]