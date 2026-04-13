"""
website/sitemaps.py

Sitemap classes for all public-facing content.
Compatible with Google Search Console XML sitemap protocol.
"""
from __future__ import annotations

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from cms.models import Page
from resources.models import ResourceItem
from website.models import Partner


class StaticViewSitemap(Sitemap):
    """Static public pages that don't come from the database."""
    priority = 1.0
    changefreq = "weekly"
    protocol = "https" if not settings.DEBUG else "http"

    def items(self):
        return ["home", "contact", "partners", "resources:list"]

    def location(self, item):
        return reverse(item)


class PageSitemap(Sitemap):
    """CMS Pages — only published ones."""
    priority = 0.8
    changefreq = "weekly"
    protocol = "https" if not settings.DEBUG else "http"

    def items(self):
        return Page.objects.filter(is_published=True).only("slug", "updated_at")

    def location(self, obj):
        return reverse("cms:page_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj):
        return obj.updated_at


class ResourceSitemap(Sitemap):
    """All ResourceItems (free + premium — both are indexable)."""
    priority = 0.9
    changefreq = "daily"
    protocol = "https" if not settings.DEBUG else "http"

    def items(self):
        return ResourceItem.objects.all().only("slug", "updated_at").order_by("-created_at")

    def location(self, obj):
        return reverse("resources:resource_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj):
        return obj.updated_at


class ResourceTypeSitemap(Sitemap):
    """Resource type details sitemap"""
    priority = 0.7
    changefreq = "weekly"
    protocol = "https" if not settings.DEBUG else "http"

    def items(self):
        return ResourceItem.objects.all().only("resource_type", "updated_at").order_by("-updated_at")

    def location(self, obj):
        return reverse("resources:type_detail", kwargs={"resource_type": obj.resource_type})

    def lastmod(self, obj):
        return obj.updated_at


class PartnerSitemap(Sitemap):
    """Public partner entries."""
    priority = 0.5
    changefreq = "monthly"
    protocol = "https" if not settings.DEBUG else "http"

    def items(self):
        return Partner.objects.all().only("id", "name")

    def location(self, obj):
        return reverse("partners")


# Registry used in cbe_res_hub/urls.py
sitemaps = {
    "static": StaticViewSitemap,
    "pages": PageSitemap,
    "resources": ResourceSitemap,
    "partners": PartnerSitemap,
    "resource_types": ResourceTypeSitemap,
}
