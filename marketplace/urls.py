from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('',                          views.listing_browse,  name='browse'),
    path('sell/',                     views.create_listing,  name='create'),
    path('<int:listing_id>/',         views.listing_detail,  name='detail'),
    path('<int:listing_id>/sold/',    views.mark_sold,       name='sold'),
    path('<int:listing_id>/report/',  views.report_listing,  name='report'),
]