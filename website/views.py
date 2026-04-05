"""
website/views.py

Public-facing homepage and contact page views.
"""
from __future__ import annotations

from typing import Any

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import FormView, TemplateView

from resources.models import EducationLevel, LearningArea, ResourceItem
from website.forms import ContactForm


class HomePageView(TemplateView):
    template_name = "website/home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

        # Latest 8 free resources for hero cards
        ctx["featured_resources"] = (
            ResourceItem.objects.select_related(
                "grade", "grade__level", "learning_area"
            )
            .filter(is_free=True)
            .order_by("-created_at")[:8]
        )

        # Stats strip
        ctx["total_resources"]    = ResourceItem.objects.count()
        ctx["total_levels"]       = EducationLevel.objects.count()
        ctx["total_areas"]        = LearningArea.objects.count()
        ctx["education_levels"]   = (
            EducationLevel.objects.prefetch_related("grades").order_by("order")
        )
        return ctx


class ContactView(FormView):
    template_name = "website/contact.html"
    form_class = ContactForm

    def get_success_url(self):
        from django.urls import reverse
        return reverse("contact")

    def form_valid(self, form):
        data = form.cleaned_data
        support_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@cberesourcehub.co.ke")

        # Send email notification to site admin
        try:
            send_mail(
                subject=f"[CBE Hub Contact] {data['subject']}",
                message=(
                    f"From: {data['name']} <{data['email']}>\n\n"
                    f"{data['message']}"
                ),
                from_email=support_email,
                recipient_list=[support_email],
                fail_silently=True,
            )
        except Exception:
            pass  # never crash the user experience on email failure

        messages.success(
            self.request,
            f"Thanks {data['name']}. Your message has been received. We'll get back to you shortly.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please fix the errors below and try again.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["default_topics"] = [
            "Resource upload & sharing guidelines",
            "Becoming a verified content creator",
            "Curriculum alignment questions",
            "Reporting inappropriate content",
            "Technical issues or bugs",
            "Partnership & collaboration",
        ]
        return ctx

