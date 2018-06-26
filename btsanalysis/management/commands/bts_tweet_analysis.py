from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db import transaction

from tweetdb.models import Tweet
from btsanalysis.models import Downtime, Status
from classifier import bts_classifier

CLASSIFIER_MAP = {None: None, "normal": Status.NORMAL, "disrupted": Status.BREAKDOWN, "delay": Status.DELAYED}


class Command(BaseCommand):
    help = "Analyse tweet for BTS breakdown"

    def add_arguments(self, parser):
        parser.add_argument("--wipe", help="Wipe old data", action="store_true")

    def handle(self, *args, **options):
        if options["wipe"]:
            last_span = None
        else:
            last_span = Downtime.objects.order_by("-start").first()

        query = Q()

        if last_span:
            query = Q(created_time__gt=last_span.end or last_span.start)

        query = Tweet.objects.filter(query).order_by("created_time")

        self.stdout.write(f"Loaded a span: {last_span}")

        with transaction.atomic():
            if options["wipe"]:
                self.stdout.write(self.style.ERROR("Wiping spans"))
                Downtime.objects.all().delete()

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
        result = bts_classifier.classify(item.message)
        return CLASSIFIER_MAP[result]
