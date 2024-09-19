from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import BloodDonationRequest
from django.core.exceptions import PermissionDenied


# CreateView for creating a new blood donation request
class BloodDonationRequestCreateView(CreateView):
    model = BloodDonationRequest
    fields = ['request_type', 'blood_type', 'region', 'province', 'municipality']
    template_name = 'blood/blood_donation_request_form.html'
    success_url = reverse_lazy('blood:blood-list')  # Fixed this to 'blood-list'

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.cleaned_data['request_type'] == 'donating':
            # Autofill user profile information
            profile = self.request.user.profile
            form.instance.blood_type = profile.blood_type
            form.instance.region = profile.region
            form.instance.province = profile.province
            form.instance.municipality = profile.municipality

            # Check if the user is available to donate
            if not profile.availability:
                form.add_error('request_type',
                               'You cannot create a donation request because your availability is set to False.')
                return self.form_invalid(form)
        return super().form_valid(form)


# ListView for displaying a list of blood donation requests
class BloodDonationRequestListView(ListView):
    model = BloodDonationRequest
    template_name = 'blood/blood_donation_request_list.html'
    context_object_name = 'blood_donation_requests'


# DetailView for displaying details of a single blood donation request
class BloodDonationRequestDetailView(DetailView):
    model = BloodDonationRequest
    template_name = 'blood/blood_donation_request_detail.html'
    context_object_name = 'blood_donation_request'


# UpdateView for editing an existing blood donation request
class BloodDonationRequestUpdateView(UpdateView):
    model = BloodDonationRequest
    fields = ['request_type', 'blood_type', 'region', 'province', 'municipality']
    template_name = 'blood/blood_donation_request_form.html'
    success_url = reverse_lazy('blood:blood-list')  # Fixed this to 'blood-list'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Restrict the user from updating if their availability is False for 'donating' type
        if obj.request_type == 'donating' and not self.request.user.profile.availability:
            raise ValueError('You cannot edit a donation request because your availability is set to False.')
        return obj

    def form_valid(self, form):
        if form.cleaned_data['request_type'] == 'donating':
            profile = self.request.user.profile
            # Autofill based on user's profile for 'donating'
            form.instance.blood_type = profile.blood_type
            form.instance.region = profile.region
            form.instance.province = profile.province
            form.instance.municipality = profile.municipality
        return super().form_valid(form)


class BloodDonationRequestDeleteView(DeleteView):
    model = BloodDonationRequest
    template_name = 'blood/blood_donation_request_confirm_delete.html'
    success_url = reverse_lazy('blood:blood-list')  # Fixed this to 'blood-list'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Restrict deletion to the user who created the request
        if obj.user != self.request.user:
            raise PermissionDenied('You do not have permission to delete this request.')
        return obj