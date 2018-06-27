import datetime

from django.views.generic import TemplateView
from django.core.cache import cache
from django.db.models import Q
from django.utils import timezone

from . import models

SECONDS_IN_MONTH = float(30 * 24 * 60 * 60)


class CurrentStatus(TemplateView):
    template_name = "current_status.html"

    def get_context_data(self, **kwargs):
        out = super().get_context_data(**kwargs)

        out["span"] = models.Downtime.objects.order_by("-start").first()
        last_updated = cache.get("tweetdb:last_update")
        if last_updated:
            last_updated = datetime.datetime.fromtimestamp(last_updated, tz=timezone.utc)
        out["last_updated"] = last_updated

        start = timezone.now() - datetime.timedelta(days=30)
        previous_spans = list(self.get_previous_spans(start))

        for item in previous_spans:
            item.display_left = ((item.start - start).total_seconds() / SECONDS_IN_MONTH) * 100
            item.display_width = (item.get_duration() / SECONDS_IN_MONTH) * 100

            if item.display_left < 0:
                item.display_width = item.display_width + item.display_left
                item.display_left = 0

        out["previous_spans"] = previous_spans
        out["previous_start"] = start
        out["sla"] = self.compute_sla(start, previous_spans)

        return out

    def get_previous_spans(self, start):
        return models.Downtime.objects.order_by("start").filter(Q(end=None) | Q(end__gte=start)).select_related()

    def compute_sla(self, start, spans):
        working = SECONDS_IN_MONTH

        # BTS operation time is from 6-24, so 6 hours per day are free
        working -= 30 * 6 * 60 * 60

        for item in spans:
            loss = item.get_duration()
            # If this item is before the start of range, then return the credit back
            before_start = min(0, (item.start - start).total_seconds())
            loss += before_start
            working -= loss

        return (working / SECONDS_IN_MONTH) * 100
