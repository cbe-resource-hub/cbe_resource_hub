"""
Celery configuration for CBE Resources Hub project.

Design goals:
- Prevent task pile-ups after restart
- Preserve existing task names and behavior

Key principles used:
- Expiration on time-sensitive tasks
- Load staggering to reduce DB and CPU spikes
"""

import os
from celery import Celery
from celery.schedules import crontab

# ------------------------------------------------------------------------------
# Django settings
# ------------------------------------------------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbe_res_hub.settings")

app = Celery("cbe_res_hub")

# Load settings from Django with CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks.py from installed apps
app.autodiscover_tasks()

# ------------------------------------------------------------------------------
# Time configuration
# ------------------------------------------------------------------------------
# Use local time to match business logic and ops expectations
app.conf.timezone = "Africa/Nairobi"
app.conf.enable_utc = False

# ------------------------------------------------------------------------------
# Celery Beat schedule
# ------------------------------------------------------------------------------
# IMPORTANT:
# - All nightly tasks have `expires` to avoid post-deploy pileups
# - Tasks are staggered to avoid DB contention
# ------------------------------------------------------------------------------

app.conf.beat_schedule = {

}
