from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.contrib import messages
from django.db import models
from blood.models import BloodDonationRequest
from account.models import CustomUser


# Decorator to check if the user is an admin
def admin_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_staff)(view_func)
    return decorated_view_func


@admin_required
def admin_dashboard(request):
    total_users = CustomUser.objects.count()
    total_donations = BloodDonationRequest.objects.count()
    donations_by_type = BloodDonationRequest.objects.values('request_type').annotate(count=models.Count('id'))

    context = {
        'total_users': total_users,
        'total_donations': total_donations,
        'donations_by_type': donations_by_type,
    }
    return render(request, 'admin_dashboard/dashboard.html', context)


# Example View 2: List All Users
@admin_required
def list_users(request):
    users = CustomUser.objects.all()
    return render(request, 'admin_dashboard/list_users.html', {'users': users})


# Example View 3: Delete a User (with confirmation)
@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect(reverse('admin-list-users'))
    return render(request, 'admin_dashboard/delete_user_confirm.html', {'user': user})
