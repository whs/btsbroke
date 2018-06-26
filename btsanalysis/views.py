import datetime

from django.views.generic import TemplateView
from django.core.cache import cache

from . import models


class CurrentStatus(TemplateView):
    template_name = "current_status.html"

    def get_context_data(self, **kwargs):
        out = super().get_context_data(**kwargs)

        out["span"] = models.Downtime.objects.order_by("-start").first()
        last_updated = cache.get("tweetdb:last_update")
        if last_updated:
            last_updated = datetime.datetime.fromtimestamp(last_updated)
        out["last_updated"] = last_updated

        return out
