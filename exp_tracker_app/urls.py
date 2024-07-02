from django.urls import path
from .views import *


app_name = 'exp_tracker_app'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('register', register, name='register'),
    path('login', login_view, name='login'),
    path('create_expense', create_expense, name='create_expense'),
    path('profile', profile, name='profile'),
    path('logout_from_app', logout_from_app, name='logout_from_app'),
]