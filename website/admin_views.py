from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, DetailView

from accounts.admin_views import IsAdminMixin
from accounts.models import CustomUser
from cms.models import Page
from resources.models import ResourceItem
from website.models import ContactMessage, Partner


# ── Dashboard ────────────────────────────────────────────────────────────────
class AdminDashboardView(IsAdminMixin, TemplateView):
    template_name = "admin/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["total_users"] = CustomUser.objects.count()
        ctx["total_vendors"] = CustomUser.objects.filter(role=CustomUser.Role.VENDOR).count()
        ctx["total_resources"] = ResourceItem.objects.count()
        ctx["total_pages"] = Page.objects.count()
        ctx["unread_messages"] = ContactMessage.objects.filter(is_read=False).count()

        ctx["recent_users"] = CustomUser.objects.order_by("-date_joined")[:5]
        ctx["recent_resources"] = ResourceItem.objects.select_related("vendor").order_by("-created_at")[:5]
        return ctx


# ── Contact Messages ─────────────────────────────────────────────────────────

class AdminContactMessageListView(IsAdminMixin, ListView):
    model = ContactMessage
    template_name = "admin/contact_message_list.html"
    context_object_name = "contact_messages"
    paginate_by = 20
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["unread_count"] = ContactMessage.objects.filter(is_read=False).count()
        return ctx


class AdminContactMessageDetailView(IsAdminMixin, DetailView):
    model = ContactMessage
    template_name = "admin/contact_message_detail.html"
    context_object_name = "msg"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # auto-mark as read when admin opens it
        obj = self.get_object()
        if not obj.is_read:
            obj.is_read = True
            obj.save(update_fields=["is_read"])
        return response


class AdminContactMessageDeleteView(IsAdminMixin, DeleteView):
    model = ContactMessage
    success_url = reverse_lazy("management:contact_list")

    def form_valid(self, form):
        messages.success(self.request, "Contact message deleted.")
        return super().form_valid(form)


# ── Partners ─────────────────────────────────────────────────────────────────
class AdminPartnerListView(IsAdminMixin, ListView):
    model = Partner
    template_name = "admin/partner_list.html"
    context_object_name = "partners"
    paginate_by = 30
    ordering = ["name"]


class AdminPartnerCreateView(IsAdminMixin, CreateView):
    model = Partner
    template_name = "admin/seo_form.html"
    fields = ["name", "slug", "link", "description", "logo", "show_as_banner", "banner_cta",
              "meta_title", "meta_description", "meta_keywords", "featured_image"]
    success_url = reverse_lazy("management:partner_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "Add New Partner"
        ctx["cancel_url"] = self.success_url
        ctx["parent_title"] = "Partners"
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f"Partner '{form.instance.name}' added successfully.")
        return super().form_valid(form)


class AdminPartnerUpdateView(IsAdminMixin, UpdateView):
    model = Partner
    template_name = "admin/seo_form.html"
    fields = ["name", "slug", "link", "description", "logo", "show_as_banner", "banner_cta",
              "meta_title", "meta_description", "meta_keywords", "featured_image"]
    success_url = reverse_lazy("management:partner_list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = f"Edit Partner: {self.object.name}"
        ctx["cancel_url"] = self.success_url
        ctx["parent_title"] = "Partners"
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Partner updated successfully.")
        return super().form_valid(form)


class AdminPartnerDeleteView(IsAdminMixin, DeleteView):
    model = Partner
    success_url = reverse_lazy("management:partner_list")

    def form_valid(self, form):
        messages.success(self.request, "Partner deleted.")
        return super().form_valid(form)
