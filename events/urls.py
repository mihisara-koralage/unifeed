from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('',                             views.event_list,      name='list'),
    path('create/',                      views.create_event,    name='create'),
    path('<int:event_id>/',              views.event_detail,    name='detail'),
    path('<int:event_id>/rsvp/<str:status>/', views.rsvp_toggle, name='rsvp'),
    path('<int:event_id>/dashboard/',    views.rsvp_dashboard,  name='dashboard'),
]