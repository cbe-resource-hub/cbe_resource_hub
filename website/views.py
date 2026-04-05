"""
website/views.py

Public-facing homepage view.

The homepage renders a Hero section with featured/latest resources
and a quick stats strip. It reuses the same ResourceItem queryset
optimisations as ResourceListView.
"""
from __future__ import annotations

from typing import Any

from django.views.generic import TemplateView

from resources.models import EducationLevel, LearningArea, ResourceItem


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
