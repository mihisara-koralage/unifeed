from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('profile/',  views.profile_view,  name='profile'),

    # Password change
    path('password/change/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/password_change.html',
            success_url='/users/password/change/done/'
        ),
        name='password_change'
    ),
    path('password/change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done'
    ),
]