"""accounts/views.py"""
from __future__ import annotations

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django import forms
from django.contrib import messages

from .models import CustomUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model  = CustomUser
        fields = ["first_name", "last_name", "phone_number"]
        widgets = {
            "first_name":   forms.TextInput(attrs={"class": "form-input"}),
            "last_name":    forms.TextInput(attrs={"class": "form-input"}),
            "phone_number": forms.TextInput(attrs={"class": "form-input"}),
        }


class DashboardView(LoginRequiredMixin, TemplateView):
    """Authenticated user dashboard — overview of account + recent activity."""
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        # Resources uploaded by this user (vendor context)
        from resources.models import ResourceItem
        ctx["my_resources"] = (
            ResourceItem.objects.select_related("grade", "grade__level", "learning_area")
            .filter(vendor=user)
            .order_by("-created_at")[:10]
        )
        ctx["my_resource_count"] = ResourceItem.objects.filter(vendor=user).count()

        # Allauth email verification status
        try:
            from allauth.account.models import EmailAddress
            ctx["email_verified"] = EmailAddress.objects.filter(
                user=user, verified=True
            ).exists()
        except Exception:
            ctx["email_verified"] = False

        return ctx


class ProfileView(LoginRequiredMixin, UpdateView):
    """Edit own profile — name + phone number."""
    model         = CustomUser
    form_class    = ProfileForm
    template_name = "accounts/profile.html"
    success_url   = reverse_lazy("accounts:dashboard")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)
