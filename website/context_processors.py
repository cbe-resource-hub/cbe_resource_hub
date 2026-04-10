"""
website/context_processors.py

Global context injected into every template request.
"""
from __future__ import annotations


def partner_banners(request):
    """
    Inject active banner partners into all templates.
    Uses select_related to minimise queries.
    Cached in the request to avoid duplicate queries if called multiple times.
    """
    from django.core.cache import cache
    from website.models import Partner

    cache_key = "active_partner_banners"
    banners = cache.get(cache_key)

    if banners is None:
        banners = list(
            Partner.objects.filter(show_as_banner=True)
            .only("name", "link", "logo", "featured_image", "banner_cta")
            .order_by("name")
        )
        # Cache for 5 minutes — short enough to pick up changes quickly
        cache.set(cache_key, banners, 300)

    return {"partner_banners": banners}
