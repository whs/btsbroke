from rest_framework import serializers
from enumfields.drf import EnumSupportSerializerMixin

from . import models
from tweetdb.models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source="get_absolute_url")

    class Meta:
        model = Tweet
        fields = ("user", "created_time", "message", "url")


class DowntimeSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    tweet_start = TweetSerializer()
    tweet_end = TweetSerializer()

    enumfield_options = {"ints_as_names": True}

    class Meta:
        model = models.Downtime
        fields = ("status", "tweet_start", "tweet_end", "start", "end")
