from django.contrib import admin

from .models import Tweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    date_hierarchy = "created_time"
    list_display = ("user", "created_time", "message")
    list_filter = ("user",)
