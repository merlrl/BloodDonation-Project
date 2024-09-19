from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import BloodDonationRequest
from .forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from .forms import ProfileForm
from .models import Profile
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to profile creation after registration
            return redirect('create_profile')  # Assuming 'create_profile' is the URL name for profile creation view
    else:
        form = UserRegistrationForm()

    return render(request, 'account/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            profile, created = Profile.objects.get_or_create(user=user)

            # Redirect to create profile if it is incomplete
            if not profile.first_name or not profile.last_name:
                return redirect('create_profile')

            login(request, user)
            return redirect('home')
        else:
            return render(request, 'account/login.html', {'error': 'Invalid credentials'})
    return render(request, 'account/login.html')


@login_required
def create_profile_view(request):
    # Try to get the profile, or create it if it does not exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # Or wherever you want to redirect

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'account/create_profile.html', {'form': form})



def home(request):
    return render(request, 'home.html')  # Render a template named 'home.html'


@login_required
def profile_page(request):
    profile = request.user.profile  # Accessing the related profile
    blood_requests = BloodDonationRequest.objects.filter(user=request.user)  # Get blood donation requests for this user

    context = {
        'profile': profile,
        'blood_requests': blood_requests,
    }

    return render(request, 'account/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'account/profile_update.html'

    def get_object(self):
        # Get the profile associated with the logged-in user
        return self.request.user.profile

    def form_valid(self, form):
        # Restrict changes to the availability field
        availability = form.cleaned_data.get('availability')
        last_donation_date = form.cleaned_data.get('last_donation_date')

        # If the user is trying to set availability to True, check the last donation date
        if availability and last_donation_date:
            days_since_donation = (timezone.now().date() - last_donation_date).days
            if days_since_donation < 56:
                form.add_error('availability', ValidationError(
                    f"You need to wait {56 - days_since_donation} more days before donating again."))
                return self.form_invalid(form)

        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['blood_type'].disabled = True  # Disable blood type field, users can't change it
        return form

    def get_success_url(self):
        return reverse('profile')


@login_required
def profile_view(request):
    # Get the profile, create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {
        'profile': profile,
    }
    return render(request, 'account/profile.html', context)
