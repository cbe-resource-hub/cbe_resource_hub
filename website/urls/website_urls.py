from django.urls import path

from website.health_checks import health_check, liveness_check, readiness_check, celery_health
from website.views import HomePageView, ContactView, PartnerListView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("partners/", PartnerListView.as_view(), name="partners"),

    # Health check endpoints
    path('health/', health_check, name='health_check'),
    path('health/live/', liveness_check, name='liveness'),
    path('health/ready/', readiness_check, name='readiness'),
    path('health/celery/', celery_health, name='celery_health'),

]
