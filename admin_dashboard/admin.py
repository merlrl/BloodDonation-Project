from django.contrib import admin
from account.models import CustomUser, Profile
from blood.models import BloodDonationRequest

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(BloodDonationRequest)
