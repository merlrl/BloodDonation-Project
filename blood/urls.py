from django.urls import path
from .views import (
    BloodDonationRequestCreateView,
    BloodDonationRequestListView,
    BloodDonationRequestDetailView,
    BloodDonationRequestUpdateView,
    BloodDonationRequestDeleteView,
)
app_name = 'blood'

urlpatterns = [
    path('create/', BloodDonationRequestCreateView.as_view(), name='blood-create'),
    path('', BloodDonationRequestListView.as_view(), name='blood-list'),
    path('<int:pk>/', BloodDonationRequestDetailView.as_view(), name='blood-detail'),
    path('<int:pk>/update/', BloodDonationRequestUpdateView.as_view(), name='blood-update'),
    path('<int:pk>/delete/', BloodDonationRequestDeleteView.as_view(), name='blood-delete'),
]
