from django.db import models


class Tweet(models.Model):
    user = models.CharField(max_length=15, db_index=True)
    created_time = models.DateTimeField(db_index=True)
    message = models.CharField(max_length=240)

    def __str__(self):
        return f"<Tweet {self.id}>"

    def get_absolute_url(self):
        return f"https://twitter.com/{self.user}/status/{self.id}"
