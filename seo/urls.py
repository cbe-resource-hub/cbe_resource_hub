from django.urls import path

from seo import admin_views

urlpatterns = [
    # SEO Management
    path("", admin_views.AdminSlugRedirectListView.as_view(), name="seo_redirect_list"),
    path("add/", admin_views.AdminSlugRedirectCreateView.as_view(), name="seo_redirect_add"),
    path("<int:pk>/edit/", admin_views.AdminSlugRedirectUpdateView.as_view(), name="seo_redirect_edit"),
    path("<int:pk>/delete/", admin_views.AdminSlugRedirectDeleteView.as_view(), name="seo_redirect_delete"),
    path("audit/", admin_views.AdminSEOAuditView.as_view(), name="seo_audit"),

]
