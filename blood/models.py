from django.db import models
from account.models import CustomUser
from django.conf import settings
from django.contrib.auth.models import User  # Assuming you're using Django's User model


class BloodDonationRequest(models.Model):
    REQUEST_TYPES = [
        ('donating', 'Donating'),
        ('looking', 'Looking'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blood_blood_requests')
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES)
    blood_type = models.CharField(max_length=3)
    region = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.request_type}'

    def get_absolute_url(self):
        return reverse('blood:donation_detail', kwargs={'pk': self.pk})  # Define this later
