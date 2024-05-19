from django.urls import path
from .views import register, login_view


app_name = 'exp_tracker_app'

urlpatterns = [
    path('register', register, name='register'),
    path('login', login_view, name='login'),
]