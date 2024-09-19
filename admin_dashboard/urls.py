from django.urls import path
from .views import admin_dashboard, list_users, delete_user

urlpatterns = [
    path('', admin_dashboard, name='admin-dashboard'),
    path('users/', list_users, name='admin-list-users'),
    path('users/delete/<int:user_id>/', delete_user, name='admin-delete-user'),
]

