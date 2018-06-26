import time
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.db import transaction, IntegrityError
import twitter

from tweetdb.models import Tweet


class Command(BaseCommand):
    help = "Update tweets"

    def handle(self, *args, **options):
        assert settings.TWITTER_CONSUMER_KEY, "TWITTER_CONSUMER_KEY must be set"
        assert settings.TWITTER_CONSUMER_SECRET, "TWITTER_CONSUMER_SECRET must be set"
        assert settings.TWITTER_ACCESS_TOKEN, "TWITTER_ACCESS_TOKEN must be set"
        assert (
            settings.TWITTER_ACCESS_TOKEN_SECRET
        ), "TWITTER_ACCESS_TOKEN_SECRET must be set"

        client = twitter.Api(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token_key=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
            sleep_on_rate_limit=True,
            tweet_mode="extended",
        )

        last_id = Tweet.objects.only("id").order_by("-created_time").first()
        last_id = last_id.id if last_id else None
        max_id = None
        tweets = []
        found_id = set()

        with transaction.atomic():
            while True:
                load_count = 200
                processed = 0

                if last_id:
                    self.stdout.write(f"Loading tweets since {last_id}...")
                elif max_id:
                    self.stdout.write(f"Loading tweets before {max_id}...")
                else:
                    self.stdout.write(f"Loading tweets...")

                statuses = client.GetUserTimeline(
                    screen_name="BTS_SkyTrain",
                    since_id=last_id,
                    max_id=max_id,
                    count=load_count,
                    include_rts=False,
                    trim_user=True,
                    exclude_replies=True,
                )
                self.stdout.write(self.style.SUCCESS(f"Loaded {len(statuses)} tweets"))

                for item in statuses:
                    if item.id in found_id:
                        continue

                    created = datetime.datetime.fromtimestamp(
                        item.created_at_in_seconds, tz=datetime.timezone.utc
                    )
                    with transaction.atomic():
                        # Use savepoint to indicate that we don't care
                        # about errors
                        try:
                            Tweet(
                                id=item.id,
                                created_time=created,
                                message=item.full_text,
                                user="BTS_SkyTrain",
                            ).save()
                        except IntegrityError:
                            pass

                    max_id = item.id
                    last_id = None
                    found_id.add(item.id)
                    processed += 1

                if processed == 0:
                    break

        cache.set("tweetdb:last_update", time.time())
