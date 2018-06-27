from enum import Enum

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from enumfields import EnumIntegerField


class Status(Enum):
    NORMAL = 1
    DELAYED = 2
    BREAKDOWN = 3

    def as_human_string(self):
        string_map = {Status.NORMAL: "ปกติ", Status.DELAYED: "ล่าช้า", Status.BREAKDOWN: "เสีย"}
        return string_map[self]

    def as_bootstrap_class(self):
        string_map = {Status.NORMAL: "bg-success", Status.DELAYED: "bg-warning", Status.BREAKDOWN: "bg-danger"}
        return string_map[self]


def validate_not_normal(value):
    if value is Status.NORMAL:
        raise ValidationError("Don't store normal status in database")


class Downtime(models.Model):
    status = EnumIntegerField(Status, validators=[validate_not_normal])
    tweet_start = models.ForeignKey("tweetdb.Tweet", on_delete=models.CASCADE, related_name="+")
    tweet_end = models.ForeignKey("tweetdb.Tweet", blank=True, null=True, on_delete=models.SET_NULL, related_name="+")
    # This is denormalized for performance
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)

    def get_latest_status(self):
        if self.end is not None:
            return Status.NORMAL
        else:
            return self.status

    def get_duration(self):
        target = self.end or timezone.now()
        return (target - self.start).total_seconds()

    def __str__(self):
        return f"{self.status.name} from {self.start} - {self.end}"
