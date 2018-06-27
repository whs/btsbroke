from django.contrib import admin

from .models import Downtime


@admin.register(Downtime)
class DowntimeAdmin(admin.ModelAdmin):
    date_hierarchy = "start"
    list_display = ("status", "start", "end")
    list_filter = ("status",)
    raw_id_fields = ("tweet_start", "tweet_end")
