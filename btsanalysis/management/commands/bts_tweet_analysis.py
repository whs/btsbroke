import re

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db import transaction

from tweetdb.models import Tweet
from btsanalysis.models import Downtime, Status

NORMAL_REGEX = re.compile(r"ปกติ")
DELAYED_REGEX = re.compile(r"ล่าช้า")
BREAKDOWN_REGEX = re.compile(r"ขัดข้อง")


class Command(BaseCommand):
    help = "Analyse tweet for BTS breakdown"

    def handle(self, *args, **options):
        last_span = Downtime.objects.order_by("-start").first()
        query = Q()

        if last_span:
            query = Q(created_time__gt=last_span.end or last_span.start)

        query = Tweet.objects.filter(query).order_by("created_time")

        self.stdout.write(f"Loaded a span: {last_span}")

        with transaction.atomic():
            for item in query:
                tweet_type = self.analyze(item)
                if tweet_type is None:
                    # Noise
                    continue

                last_span_status = last_span.get_latest_status() if last_span else Status.NORMAL
                if tweet_type == last_span_status:
                    # Nothing to update
                    continue

                # Something changed...
                # Is the current breakdown ended?
                if last_span and last_span.end is None and tweet_type is Status.NORMAL:
                    last_span.tweet_end = item
                    last_span.end = item.created_time
                    last_span.save()
                    self.stdout.write(f"Span ended: {last_span}")
                # Breakdown changed status
                else:
                    if last_span and last_span.end is None:
                        last_span.tweet_end = item
                        last_span.end = item.created_time
                        last_span.save()

                    new_span = Downtime(status=tweet_type, tweet_start=item, start=item.created_time)
                    new_span.save()
                    self.stdout.write(f"New span: {new_span.status.name}")
                    last_span = new_span

    def analyze(self, item):
        if BREAKDOWN_REGEX.search(item.message):
            # ระบบอาณัติสัญญาณในสายสีลมและสายสุขุมวิทขัดข้อง  กำลังทำการแก้ไข ขบวนรถจะล่าช้า 10 นาที ขออภัยในความไม่สะดวก
            return Status.BREAKDOWN
        elif DELAYED_REGEX.search(item.message):
            return Status.DELAYED
        elif NORMAL_REGEX.search(item.message):
            return Status.NORMAL

        return None
