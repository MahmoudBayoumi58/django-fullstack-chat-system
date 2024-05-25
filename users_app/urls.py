from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('activate/<str:code>/', activate_account, name='activate'),
    path('activation/send', activation_request_view, name='send_activation_view'),
    path('forget-password/', forget_password_view, name='forget_password'),
    path('reset-password/<str:code>/', reset_password_view, name='reset_password'),
    path('change-password/', change_password_view, name='change_password'),
    path('dashboard', dashboard_view, name='dashboard'),
    path('suggested-users', suggested_users_view, name='suggested_users'),
    path('settings', settings_view, name='user_settings'),
    path('info-update/', update_user_view, name='update_user_info'),
]
