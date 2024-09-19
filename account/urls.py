from django.urls import path
from django.contrib.auth import views as auth_views  # <-- Add this line
from .views import register, home, create_profile_view, login_view, ProfileUpdateView  # Import your views
from .import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page URL pattern
    path('register/', register, name='register'),  # Registration URL pattern
    path('login/', login_view, name='login'),  # Login URL pattern
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('create-profile/', create_profile_view, name='create_profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/', views.profile_page, name='profile'),


]
